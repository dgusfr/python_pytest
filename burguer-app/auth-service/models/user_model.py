def serialize_user(user):
    """
    Serializa um dict de usuário para um formato JSON da resposta.
    args:
      - user: dict contendo os dados do usuário do banco de dados
    returns:
      - dict com os campos relevantes do usuário para resposta JSON
    """
    return {
        "email": user.get("email"),
        "name": user.get("name", ""),
        "address": user.get("address", ""),
        "role": user.get("role", "cliente"),
    }
