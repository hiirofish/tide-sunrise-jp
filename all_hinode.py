import os
from datetime import datetime, timedelta
import ephem
from zoneinfo import ZoneInfo

def generate_hinode_data(year, output_dir, file_path='keisai.tsv'):
    """日の出日の入りデータを生成する関数"""
    
    # 日本のタイムゾーン
    jst = ZoneInfo("Asia/Tokyo")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        next(f)
        total_lines = sum(1 for _ in open(file_path, 'r', encoding='utf-8')) - 1
        processed = 0

        for line in f:
            items = line.strip().split('\t')
            location_code = items[1].lower()
            
            # 緯度と経度を度単位で取得
            lat_deg = float(items[3].split('゜')[0])
            lat_min = float(items[3].split('゜')[1].split("'")[0])
            latitude = lat_deg + lat_min/60.0
            
            lon_deg = float(items[4].split('゜')[0])
            lon_min = float(items[4].split('゜')[1].split("'")[0])
            longitude = lon_deg + lon_min/60.0

            # 観測地点の設定
            observer = ephem.Observer()
            observer.lat = str(latitude)  # 緯度を文字列で設定
            observer.lon = str(longitude)  # 経度を文字列で設定
            observer.elevation = 0  # 標高（メートル）
            observer.pressure = 0  # 大気圧の影響を無視
            observer.horizon = '-0:34'  # 標準的な地平線補正

            filename = os.path.join(output_dir, f'hinode_{year}_{location_code}_hinode.txt')

            with open(filename, 'w', encoding='utf-8') as out_file:
                date = datetime.strptime(f'{year}-01-01', '%Y-%m-%d').date()
                end_date = datetime.strptime(f'{year}-12-31', '%Y-%m-%d').date()

                while date <= end_date:
                    # 日付を設定
                    observer.date = date.strftime('%Y/%m/%d')
                    
                    # 日の出・日の入り時刻を計算
                    sunrise = observer.next_rising(ephem.Sun())
                    sunset = observer.next_setting(ephem.Sun())

                    # UTC -> JST変換（+9時間）
                    sunrise_dt = ephem.Date(sunrise).datetime() + timedelta(hours=9)
                    sunset_dt = ephem.Date(sunset).datetime() + timedelta(hours=9)

                    # ファイルへの書き込み
                    out_file.write('{} {:02d}{:02d} {:02d}{:02d}\n'.format(
                        date.strftime('%m%d'),
                        sunrise_dt.hour,
                        sunrise_dt.minute,
                        sunset_dt.hour,
                        sunset_dt.minute
                    ))

                    date += timedelta(days=1)
            
            processed += 1
            print(f"Progress: {processed}/{total_lines} locations processed", end='\r')

        print("\nAll files have been written successfully!")

def main():
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