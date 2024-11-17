import os
import sys
import requests
import pandas as pd

def download_tide_data(year, output_dir, file_path='keisai.tsv'):
    """潮位データをダウンロードする関数"""
    
    # TSVファイルの読み込み
    df = pd.read_csv(file_path, delimiter='\t')
    
    # 地点記号のリストを作成（NaNを除外し、ユニークな地点番号を抽出）
    locations = df['地点 記号'].dropna().unique().tolist()
    total_locations = len(locations)
    processed = 0
    
    for location in locations:
        location_code = location.lower()  # 小文字に統一
        
        # URLを構築
        url = f"https://www.data.jma.go.jp/kaiyou/data/db/tide/suisan/txt/{year}/{location}.txt"
        
        try:
            # データをダウンロード
            response = requests.get(url)
            
            # レスポンスが成功した場合、データをファイルに保存
            if response.status_code == 200:
                # 新しい命名規則に従ったファイル名
                output_file = os.path.join(output_dir, f'tide_{year}_{location_code}.txt')
                
                with open(output_file, "w", encoding="utf-8") as file:
                    file.write(response.text)
            else:
                print(f"Failed to download data for location: {location}, year: {year}")
                
            # 進捗表示
            processed += 1
            print(f"Progress: {processed}/{total_locations} locations downloaded", end='\r')
                
        except requests.exceptions.RequestException as e:
            print(f"Error downloading {location}: {str(e)}")
    
    print("\nDownload completed!")

def main():
    """メイン関数"""
    try:
        if len(sys.argv) > 1:
            year = int(sys.argv[1])
        else:
            year = int(input("Enter year: "))
            
        output_dir = f'tide_{year}'
        os.makedirs(output_dir, exist_ok=True)
        
        download_tide_data(year, output_dir)
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    import sys
    main()