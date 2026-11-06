from fastapi import APIRouter, Depends
from dependecies import verificar_visitante

visitor_router = APIRouter(
    prefix="/visitante",
    tags=["visitante"],
    dependencies=[Depends(verificar_visitante)]
)


@visitor_router.get("/dashboard")
async def dashboard_visitante():
    return [
        {
            "id": 9001,
            "status": "PENDENTE",
            "preco": 75.00,
            "usuario": "Visitante",
            "itens": [
                {"quantidade": 1, "sabor": "Calabresa", "tamanho": "medio", "preco_unitario": 75.00}
            ]
        },
        {
            "id": 9002,
            "status": "FINALIZADO",
            "preco": 80.00,
            "usuario": "Visitante",
            "itens": [
                {"quantidade": 1, "sabor": "Portuguesa", "tamanho": "grande", "preco_unitario": 80.00}
            ]
        },
        {
            "id": 9003,
            "status": "PRONTO",
            "preco": 50.00,
            "usuario": "Visitante",
            "itens": [
                {"quantidade": 1, "sabor": "Marguerita", "tamanho": "pequeno", "preco_unitario": 50.00}
            ]
        },
        {
            "id": 9004,
            "status": "ENTREGUE",
            "preco": 75.00,
            "usuario": "Visitante",
            "itens": [
                {"quantidade": 1, "sabor": "Peperone", "tamanho": "medio", "preco_unitario": 75.00}
            ]
        }
    ]