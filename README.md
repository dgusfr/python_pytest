# python-testes



Execução de testes unitario e de cobertura com arquivo pytest.ini:

pytest --cov=models.user_model
pytest --cov=models.user_model --cov-report=term-missing
pytest --cov .\test\ --cov-report=term-missing
pytest --cov=models.user_model --cov-report=term-missing --cov-report=html
pytest --cov=models.user_model --cov-report=term-missing --cov-report=html --cov-fail-under=60

![alt text](images/image.png)

![alt text](images/image2.png)

MONGO_URI="mongodb+srv://diegog_db_user:pythontests123@cluster0.v7dohhh.mongodb.net/?appName=Cluster0"
SECRET_KEY="EF2D3C4B5A6978877665544332211AA00BB11CC22DD33EE44FF55GG66HH77II88"
JWT_SECRET="F4E5D6C7B8A99887766554433221100AABBCCDDFFEEDDCCBBAA99887766554433"