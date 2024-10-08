  nginx:
    build: ./nginx
    ports:
      - "80:80"
    depends_on:
      - backend
      - frontend
    restart: always