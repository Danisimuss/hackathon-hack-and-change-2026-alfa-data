from pathlib import Path
import html
import re
import pandas as pd


def clean_text(text):
    if pd.isna(text):
        return text
    text = re.sub(r'<[^>]+>', ' ', text)
    text = html.unescape(text)
    text = ' '.join(text.split())
    return text if text else pd.NA


def main():
    folder = Path(__file__).resolve().parent
    df = pd.read_csv(folder / 'data' / 'courses_raw.csv', encoding='utf-8-sig')
    print('Строк и столбцов:', df.shape)
    print('Дубли ID:', df['course_id'].duplicated().sum())

    # Исходные поля сохраняем, результаты записываем в новые столбцы.
    for column in ['title', 'description', 'target', 'topics', 'tags']:
        df[column + '_clean'] = df[column].apply(clean_text)

    placeholders = df['target_clean'].str.lower().isin(['цель', 'цель курса'])
    df.loc[placeholders, 'target_clean'] = pd.NA

    df['duration_clean'] = df['duration'].str.replace(',', '.', regex=False)
    df['duration_clean'] = df['duration_clean'].str.replace('~', '', regex=False).str.strip()
    df['duration_is_approx'] = df['duration'].str.contains('~', regex=False, na=False)

    hours = df['duration_clean'].str.extract(r'(\d+(?:\.\d+)?)\s*час', expand=False)
    minutes = df['duration_clean'].str.extract(r'(\d+)\s*мин', expand=False)
    hours = pd.to_numeric(hours)
    minutes = pd.to_numeric(minutes)
    total = hours.fillna(0) * 60 + minutes.fillna(0)
    # Если ни часы, ни минуты не найдены, результат остаётся неизвестным.
    total = total.where(hours.notna() | minutes.notna())
    df['duration_minutes'] = total.round().astype('Int64')
    df['duration_parse_error'] = df['duration'].notna() & total.isna()

    df['experience_level'] = df['experience_labels'].map({
        'Без опыта': 'beginner',
        'С опытом': 'experienced',
    }).fillna('unknown')
    df['has_new_label'] = df['experience_labels'].eq('💥 NEW')

    # Цену не заполняем нулём: доступ определяется отдельным полем.
    print('Типы доступа:\n', df['access_type'].value_counts())
    report = df.isna().sum().reset_index()
    report.columns = ['column', 'missing_count']
    print('Пропуски:\n', report[report['missing_count'] > 0])
    print('Нераспознанная длительность:', df['duration_parse_error'].sum())

    output = folder / 'output'
    output.mkdir(exist_ok=True)
    df.to_csv(output / 'courses_clean.csv', index=False, encoding='utf-8-sig')
    report.to_csv(output / 'quality_report.csv', index=False, encoding='utf-8-sig')
    print('Готово. Результаты в папке output.')


if __name__ == '__main__':
    main()
