## Instructions

### Train model
```
nohup python -u train.py --root_path=model_v0 > log/v0.log 2>&1 &
```

### Start Server
```
python -u server.py --batch_size=1 --use_beam_search=True --root_path=model_v0
```
