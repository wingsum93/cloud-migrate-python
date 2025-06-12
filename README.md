# PPP



## Commands
### default
```sh
python main.py
```

### show large files
```sh
python largest_files.py onedrive
python largest_files.py gdrive --top 50
```

### Search
```sh
python search_files_by_name.py onedrive report
python search_files_by_name.py gdrive .mp4
python search_files_by_name.py gdrive 2021
```

### move file between cloud (from g to one)
```sh
rclone copy "gdrive:tv" "onedrive:tv" --progress
  --transfers=4
  --checkers=8
  --drive-chunk-size=128M 
  --onedrive-chunk-size=100M 
  --bwlimit=10M 
  --tpslimit=10 
  --log-file=copy_tv.log 
  --log-level=INFO 
  --retries=10 
  --low-level-retries=10
```