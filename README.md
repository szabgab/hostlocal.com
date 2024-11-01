## Deployment

For some changes to take effect we need to restart uwsgi:

```
sudo systemctl restart uwsgi
```

## Development

For the development server run:

```
FLASK_APP=app FLASK_DEBUG=1 flask run --port 5000
```


Use wkhtmltopdf to convert the HTML page to PDF


## Static site

```
python app.py
rustatic --path _site/ --indexfile index.html --nice
```
