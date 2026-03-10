from langchain.tools import tool
from data import apartments


@tool
def list_available_apartments() -> str:
    """Retourne la liste des appartements disponibles."""
    available = [a for a in apartments if a["status"] == "available"]
    if not available:
        return "Aucun appartement disponible."
    
    lines = []
    for a in available:
        lines.append(
            f'{a["id"]} | bâtiment: {a["building"]} | pièces: {a["rooms"]} | loyer: {a["rent"]} MAD'
        )
    return "\n".join(lines)


@tool
def get_apartment_details(apartment_id: str) -> str:
    """Retourne les détails d'un appartement à partir de son identifiant."""
    for a in apartments:
        if a["id"].lower() == apartment_id.lower():
            return (
                f'Appartement {a["id"]}\n'
                f'Bâtiment: {a["building"]}\n'
                f'Pièces: {a["rooms"]}\n'
                f'Loyer: {a["rent"]} MAD\n'
                f'Statut: {a["status"]}\n'
                f'Locataire: {a["tenant"] or "Aucun"}'
            )
    return f"Aucun appartement trouvé avec l'identifiant {apartment_id}."


@tool
def search_apartments(max_rent: int, rooms: int) -> str:
    """Recherche les appartements disponibles selon un loyer maximum et un nombre de pièces."""
    results = [
        a for a in apartments
        if a["status"] == "available"
        and a["rent"] <= max_rent
        and a["rooms"] == rooms
    ]
    
    if not results:
        return "Aucun appartement disponible ne correspond à ces critères."
    
    lines = []
    for a in results:
        lines.append(
            f'{a["id"]} | bâtiment: {a["building"]} | pièces: {a["rooms"]} | loyer: {a["rent"]} MAD'
        )
    return "\n".join(lines)


@tool
def calculate_total_rent(apartment_ids: str) -> str:
    """
    Calcule le total des loyers pour une liste d'identifiants d'appartements.
    Format attendu: 'A101,B202'
    """
    ids = [x.strip().lower() for x in apartment_ids.split(",")]
    selected = [a for a in apartments if a["id"].lower() in ids]
    
    if not selected:
        return "Aucun appartement valide fourni."
    
    total = sum(a["rent"] for a in selected)
    details = ", ".join(f'{a["id"]}: {a["rent"]} MAD' for a in selected)
    return f"Total = {total} MAD ({details})"