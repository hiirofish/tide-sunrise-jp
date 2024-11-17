import os
import sys
from datetime import datetime
import all_hinode
import master_tide

def setup_folders(year):
    """フォルダ構造を作成"""
    base_dir = f'data_{year}'
    hinode_dir = os.path.join(base_dir, 'hinode')
    tide_dir = os.path.join(base_dir, 'tide')
    
    # フォルダが存在しない場合は作成
    for dir_path in [base_dir, hinode_dir, tide_dir]:
        os.makedirs(dir_path, exist_ok=True)
    
    return hinode_dir, tide_dir

def main():
    # コマンドライン引数から年を取得、なければ対話的に入力
    if len(sys.argv) > 1:
        try:
            year = int(sys.argv[1])
        except ValueError:
            print("Error: Year must be a number")
            sys.exit(1)
    else:
        current_year = datetime.now().year
        year = int(input(f"Enter year (current year is {current_year}): "))

    print(f"Creating data for year: {year}")
    
    try:
        # フォルダ構造のセットアップ
        hinode_dir, tide_dir = setup_folders(year)
        
        # 日の出日の入りデータの生成
        print("\nGenerating sunrise/sunset data...")
        all_hinode.generate_hinode_data(year, hinode_dir)
        
        # 潮位データの取得
        print("\nDownloading tide data...")
        master_tide.download_tide_data(year, tide_dir)
        
        print(f"\nData creation completed successfully for year {year}")
        print(f"Data stored in: data_{year}/")
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()