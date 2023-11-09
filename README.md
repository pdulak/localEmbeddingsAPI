# Qdrant and embedding - local API

The purpose of this repo is to use local embedding and Qdrant API

## How to run

1. Run the following command:

```bash
docker-compose up
```

Please note that the first run will take a while, 
as there is a few gigabytes of data to download. Also, the first
upsert to Qdrant will take a while, as the model has to be
downloaded and the index needs to be built.

2. Open `http://localhost:5000/` in your browser
3. Set up your environment by clicking "Initialize Qdrant" button
4. You can now use "upsert" to add new embeddings to the database, "test search" to 
search for the nearest neighbors of a given embedding. Please note that you should provide
UUID in the ID field.

## API reference

### `POST /upsert/`

* `ID` - UUID of the embedding (required)
* `phrase` - phrase to embed and upsert to Qdrant (required)

### `POST /search/`

* `search_term` - phrase to embed and search for nearest neighbors (required)

## Developer notes

### New packages in `requirements.txt`

When you change your `requirements.txt` file, you'll need to rebuild your Docker image to install the new Python packages. 

Here are the steps:

1. Stop the running Docker containers with the following command:

    ```bash
    docker-compose down
    ```

2. Then rebuild and start your Docker containers:

    ```bash
    docker-compose up --build
    ```
