import numpy as np
import pandas as pd

from finance_analysis import get_annualized_return
from rsi_indicator import calculate_rsi, get_lower_threshold_rsi, get_upper_threshold_rsi
from stocks_data import get_data_from_ticker


def calculate_stop_price(previous_week_low, current_week_low, previous_previous_week_low):
    return min(previous_week_low, current_week_low, previous_previous_week_low) - 0.01


def prepare_signal_data(row, index, data, target_delta):
    signal_entry_date = index
    entry_signal_rsi = row['RSI']
    entry = row['High'] + 0.01
    stop = calculate_stop_price(data.iloc[data.index.get_loc(index) - 2]['Low'],
                                data.iloc[data.index.get_loc(index) - 1]['Low'],
                                row['Low'])
    target = entry + target_delta * (entry - stop)
    return signal_entry_date, entry_signal_rsi, entry, stop, target


def add_result_to_dataframe(results, entry_signal_rsi, signal_entry_date, entry, stop, target, exit_date, exit_price):
    duration = exit_date - signal_entry_date if exit_date else pd.NaT
    result = 'Target' if exit_price >= target else ('Stop' if exit_price <= stop else 'Open')
    gain_loss_pct = ((exit_price - entry) / entry) * 100 if exit_price else np.NaN
    new_row = pd.DataFrame({'Entry RSI': [entry_signal_rsi], 'Signal Date': [signal_entry_date],
                            'Entry Date': [signal_entry_date], 'Entry': [entry], 'Stop': [stop],
                            'Target': [target], 'Exit Date': [exit_date], 'Duration': [duration],
                            'Gain/Loss %': [gain_loss_pct], 'Result': [result]})
    results = pd.concat([results, new_row], ignore_index=True)
    return results


def initialize_results_dataframe():
    columns = ['Entry RSI', 'Signal Date', 'Entry Date', 'Entry', 'Stop', 'Target',
               'Exit Date', 'Duration', 'Gain/Loss %', 'Result']
    return pd.DataFrame(columns=columns)


def backtest_rsi(ticker, target_delta, period, interval, low_threshold=0.15, use_stop=True,
                 min_holding_period=4, max_signal_period=4, use_upper_threshold=False, use_target=True):
    data = get_data_from_ticker(ticker, interval, period)
    data['RSI'] = calculate_rsi(data, period=9)
    lower_threshold = get_lower_threshold_rsi(data['RSI'], low_threshold)
    upper_threshold = get_upper_threshold_rsi(data['RSI'], 0.9)

    data['Signal'] = (data['RSI'].shift(1) <= lower_threshold) & (data['RSI'] > lower_threshold)
    data.loc[data['Signal'], 'Entry'] = data['High']
    data.loc[data['Signal'], 'Stop'] = data['Low']
    data.loc[data['Signal'], 'Target'] = data['Entry'] + target_delta * (data['Entry'] - data['Stop'])

    results = initialize_results_dataframe()

    for index, row in data[data['Signal']].iterrows():
        signal_entry_date = index
        entry_signal_rsi = row['RSI']
        entry = row['High'] + 0.01
        # Determinar o stop como 0.01 abaixo do valor mínimo entre a semana identificada e a semana anterior
        previous_previous_week_low = data.iloc[data.index.get_loc(index) - 2]['Low']
        previous_week_low = data.iloc[data.index.get_loc(index) - 1]['Low']
        current_week_low = row['Low']
        stop = min(previous_week_low, current_week_low, previous_previous_week_low) - 0.01

        target = entry + target_delta * (entry - stop)

        # Verificar se a entrada foi atingida e se o stop ou alvo foi atingido primeiro
        entry_hit = False
        hit_target = False
        hit_stop = False
        exit_date = pd.NaT
        entry_date = pd.NaT
        exit_price = np.NaN
        weeks_since_signal = 0  # Contador de semanas desde o sinal
        weeks_since_entry = -1

        stop_pct = ((stop - entry) / entry) * 100

        # Loop pelas semanas subsequentes, começando pela semana seguinte à entrada
        for week_index, week in data.loc[index + pd.Timedelta(weeks=1):].iterrows():
            weeks_since_signal += 1  # Incrementa a contagem de semanas

            if weeks_since_entry >= 0:
                weeks_since_entry += 1

            if -stop_pct > 15:
                break

            if week['Low'] <= stop and not entry_hit and \
                    ((weeks_since_signal > 1 and week[
                        'RSI'] < lower_threshold) or weeks_since_signal > max_signal_period):
                break  # Stop atingido antes da entrada, desconsidera o ponto de entrada
            if week['High'] >= entry and not entry_hit:
                entry_hit = True  # Confirma que a entrada foi atingida
                entry_date = week_index
                weeks_since_entry = 0
            if entry_hit and weeks_since_entry > min_holding_period:
                if use_upper_threshold:
                    if week['RSI'] > upper_threshold and week['Close'] >= target:
                        hit_target = True
                        exit_date = week_index
                        exit_price = week['Close']
                        break
                if week['High'] >= target and use_target:
                    hit_target = True
                    exit_date = week_index
                    if week['Open'] > target:
                        exit_price = week['Open']
                    else:
                        exit_price = target
                    break
                if week['Low'] <= stop and use_stop:
                    hit_stop = True
                    exit_date = week_index
                    if week['Open'] < stop:
                        exit_price = week['Open']
                    else:
                        exit_price = stop
                    break

        if entry_date is not pd.NaT:
            duration = exit_date - entry_date if exit_date else pd.NaT
            result = 'Target' if hit_target else ('Stop' if hit_stop else 'Open')
            gain_loss_pct = ((exit_price - entry) / entry) * 100 if exit_price is not None else np.NaN

            new_row = pd.DataFrame(
                {'Entry RSI': [entry_signal_rsi], 'Signal Date': [signal_entry_date], 'Entry Date': [entry_date],
                 'Entry': [entry], 'Stop': [stop], 'Target': [target], 'Exit Date': [exit_date], 'Duration': [duration],
                 'Gain/Loss %': [gain_loss_pct], 'Result': [result]})
            # Usar concat em vez de append
            results = pd.concat([results, new_row], ignore_index=True)

    return results


def view_backtest_results(results):
    # Configura o Pandas para exibir todas as linhas
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    # Ajusta a largura da exibição para garantir que o DataFrame não seja quebrado
    pd.set_option('display.width', 1000)
    print(results)


def get_success_rate(results):
    # Calcular a taxa de acerto
    return (results['Result'] == 'Target').sum() / len(results) * 100 if len(results) > 0 else 0


def convert_to_timedelta(item):
    if isinstance(item, str):
        return pd.to_timedelta(item, errors='coerce')
    return item


def compare_multiple_results(group_test, target_delta, period, interval, use_stop=True,
                             min_holding_period=4, max_signal_period=4, use_upper_threshold=False, use_target=True):
    comparison_results = pd.DataFrame(columns=['Ticker', 'Success Rate', 'Operations', 'Avg. Period', 'Avg. Profit'])
    for ticker in group_test:

        results = backtest_rsi(ticker, target_delta, period, interval, min_holding_period=min_holding_period,
                               use_stop=use_stop, max_signal_period=max_signal_period,
                               use_upper_threshold=use_upper_threshold, use_target=use_target)

        # Verifica se a coluna 'Duration' existe e converte para Timedelta se necessário
        if 'Duration' in results.columns and results['Duration'].dtype != 'timedelta64[ns]':
            results['Duration'] = results['Duration'].apply(convert_to_timedelta)

        # Calcula o ganho médio
        if 'Gain/Loss %' in results.columns:
            average_gain = results['Gain/Loss %'].dropna().mean()
        else:
            average_gain = None

        # Agora calcula a média da duração das operações
        if 'Duration' in results.columns:
            avg_duration = results['Duration'].dropna().mean()
            avg_period = f"{avg_duration.days} days" if not pd.isna(avg_duration) else "N/A"
            annualized_return = 100 * get_annualized_return(avg_duration.days, average_gain/100) if not pd.isna(avg_duration) else np.NaN
        else:
            avg_period = "N/A"

        new_row = pd.DataFrame({
            'Ticker': [ticker],
            'Success Rate': [get_success_rate(results)],
            'Operations': [len(results)],
            'Avg. Period': avg_period,
            'Avg. Profit': average_gain,
            'Annualized return': annualized_return})

        new_row = new_row.dropna(axis=1, how='all')
        comparison_results = pd.concat([comparison_results, new_row], ignore_index=True)

    comparison_results = comparison_results.sort_values(by='Success Rate', ascending=False).reset_index(drop=True)
    # Substitui 'N/A' por pd.NaT para permitir a conversão
    comparison_results['Avg. Period'] = comparison_results['Avg. Period'].replace('N/A', pd.NaT)

    # Agora tenta converter para Timedelta
    comparison_results['Avg. Period'] = pd.to_timedelta(comparison_results['Avg. Period'])

    return comparison_results


def make_extensive_test_tickers_list(tickers_list, period, interval, use_stop=True,
                                     min_holding_period=4, max_signal_period=4, use_upper_threshold=False, use_target=True):
    target_tests = [1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3]
    results = pd.DataFrame(columns=['Target', 'Avg. Success Rate', 'Avg. Period', 'Avg. Profit'])

    for target in target_tests:
        result = compare_multiple_results(tickers_list, target, period, interval, min_holding_period=min_holding_period,
                                          use_stop=use_stop, max_signal_period=max_signal_period,
                                          use_upper_threshold=use_upper_threshold, use_target=use_target)

        avg_success = result['Success Rate'].mean()
        avg_profit = result['Avg. Profit'].mean()
        avg_period = result['Avg. Period'].median()

        new_row = pd.DataFrame({
            'Target': [target],
            'Avg. Success Rate': [avg_success],
            'Avg. Period': avg_period,
            'Avg. Profit': avg_profit})

        results = pd.concat([results, new_row], ignore_index=True)

    return results


def make_extensive_test_ticker(ticker, period, interval, use_stop=True, min_holding_period=4, max_signal_period=4,
                               use_upper_threshold=False, use_target=True):
    tickers = [ticker]
    target_tests = [1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3]
    results = pd.DataFrame(columns=['Target', 'Avg. Success Rate', 'Avg. Period', 'Avg. Profit'])
    for tgt in target_tests:
        result = compare_multiple_results(tickers, tgt, period, interval, min_holding_period=min_holding_period,
                                          use_stop=use_stop, max_signal_period=max_signal_period,
                                          use_upper_threshold=use_upper_threshold, use_target=use_target)

        avg_success = result['Success Rate'].mean()
        avg_profit = result['Avg. Profit'].mean()
        avg_period = result['Avg. Period'].mean()
        number_operations = result['Operations'].mean()
        annualized_return = result['Annualized return'].mean()

        new_row = pd.DataFrame({
            'Target': [tgt],
            'Avg. Success Rate': [avg_success],
            'Avg. Period': avg_period,
            'No. Operations': number_operations,
            'Avg. Profit': avg_profit,
            'Annualized Return': annualized_return})

        results = pd.concat([results, new_row], ignore_index=True)

    return results
