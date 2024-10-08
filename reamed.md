  nginx:
    build: ./nginx
    ports:
      - "80:80"
    depends_on:
      - backend
      - frontend
    restart: always


    //Creacion de la database
    sudo docker exec -it some-postgres psql -U root
