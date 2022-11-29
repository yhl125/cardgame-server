# cardgame-server

## install requirements
```
pip install -r requirements.txt
```

## run server
#### localhost
```
uvicorn main:app --reload
```


## prerequisites
```
create .env file in root directory(e.g. .env.example)
intsall docker and make sure docker is running

docker pull mongo
docker run -d -p 27017:27017 mongo

If you use MongoDB Atlas instead of local MongoDB
you need to change ENV_STATE to prod, and change MONGO_URI to your MongoDB Atlas URI(mongodb+srv://...)
```

## fastapi docs
#### localhost
```
http://localhost:8000/docs
```
