# MathReader Validation

Interface used to validate the [MathReader API](https://github.com/carolreis/mathreader)

## Running it locally
```bash
virtualenv -p $(which python3) .
source bin/activate
pip install -r requirements.txt
./run
```

## Running on your Google Cloud
- Check the [app.yaml](app.yaml) file

```
gcloud init
gcloud app create
gcloud app deploy
```
