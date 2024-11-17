import os
from datetime import datetime, timedelta
from suntime import Sun, SunTimeException

def generate_hinode_data(year, output_dir, file_path='keisai.tsv'):
    """日の出日の入りデータを生成する関数"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        # ヘッダー行を読み飛ばす
        next(f)
        
        total_lines = sum(1 for _ in open(file_path, 'r', encoding='utf-8')) - 1
        processed = 0

        for line in f:
            # 行をタブで分割
            items = line.strip().split('\t')
            
            # 地点記号、緯度、経度の取得
            location_code = items[1].lower()  # 小文字に統一
            latitude = float(items[3].split('゜')[0]) + float(items[3].split('゜')[1].split("'")[0]) / 60.0
            longitude = float(items[4].split('゜')[0]) + float(items[4].split('゜')[1].split("'")[0]) / 60.0

            # ファイル名の生成（新しい形式）
            filename = os.path.join(output_dir, f'hinode_{year}_{location_code}_hinode.txt')

            # ファイルのオープン
            with open(filename, 'w', encoding='utf-8') as out_file:
                # 指定した年度の1月1日から12月31日までループ
                date = datetime.strptime(f'{year}-01-01', '%Y-%m-%d').date()
                end_date = datetime.strptime(f'{year}-12-31', '%Y-%m-%d').date()

                while date <= end_date:
                    try:
                        # 日の出・日の入りの計算
                        sun = Sun(latitude, longitude)
                        sunrise = sun.get_local_sunrise_time(date)
                        sunset = sun.get_local_sunset_time(date)

                        # ファイルへの書き込み
                        out_file.write('{} {:02d}{:02d} {:02d}{:02d}\n'.format(
                            date.strftime('%m%d'),
                            sunrise.hour,
                            sunrise.minute,
                            sunset.hour,
                            sunset.minute
                        ))
                    except SunTimeException as e:
                        print(f"Error on date {date} for location {location_code}: {e}")

                    # 次の日へ
                    date += timedelta(days=1)
            
            # 進捗表示
            processed += 1
            print(f"Progress: {processed}/{total_lines} locations processed", end='\r')

        print("\nAll files have been written successfully!")

def main():
    """メイン関数"""
    try:
        if len(sys.argv) > 1:
            year = int(sys.argv[1])
        else:
            year = int(input("Enter year: "))
            
        output_dir = f'hinode_{year}'
        os.makedirs(output_dir, exist_ok=True)
        
        generate_hinode_data(year, output_dir)
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    import sys
    main()