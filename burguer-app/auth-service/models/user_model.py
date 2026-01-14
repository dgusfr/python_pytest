"""
Este módulo contém a função de serialização para o modelo de usuário.
"""

def serialize_user(user):

    """Serializa um dicionário de usuário para um formato específico.
    Args:
        user (dict): Dicionário contendo os dados do usuário.
    Returns:
        dict: Dicionário serializado com campos específicos.
    """
    return {
        "email": user.get("email"),
        "name": user.get("name", ""),
        "address": user.get("address", ""),
        "role": user.get("role", "cliente")
    }