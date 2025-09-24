import re
import httpx
from ..config import settings

def validate_cpf_cnpj(doc: str) -> bool:
    # Fallback local: algoritmo simples para CPF/CNPJ
    doc = re.sub(r'\D', '', doc)
    if len(doc) == 11:
        return validate_cpf(doc)
    elif len(doc) == 14:
        return validate_cnpj(doc)
    return False

def validate_cpf(cpf: str) -> bool:
    if len(set(cpf)) == 1:
        return False
    sum1 = sum(int(cpf[i]) * (10 - i) for i in range(9))
    d1 = (sum1 * 10 % 11) % 10
    sum2 = sum(int(cpf[i]) * (11 - i) for i in range(10))
    d2 = (sum2 * 10 % 11) % 10
    return cpf[-2:] == f"{d1}{d2}"

def validate_cnpj(cnpj: str) -> bool:
    if len(set(cnpj)) == 1:
        return False
    weights1 = [5,4,3,2,9,8,7,6,5,4,3,2]
    weights2 = [6] + weights1
    sum1 = sum(int(cnpj[i]) * weights1[i] for i in range(12))
    d1 = 11 - sum1 % 11
    d1 = d1 if d1 < 10 else 0
    sum2 = sum(int(cnpj[i]) * weights2[i] for i in range(13))
    d2 = 11 - sum2 % 11
    d2 = d2 if d2 < 10 else 0
    return cnpj[-2:] == f"{d1}{d2}"

async def validate_doc_api(doc: str) -> bool:
    url = f"{settings.CPF_CNPJ_PUBLIC_API}{doc}"
    try:
        async with httpx.AsyncClient(timeout=2) as client:
            r = await client.get(url)
            r.raise_for_status()
            data = r.json()
            valid = bool(data.get("valid", False))
            return valid
    except Exception:
        return None  # Falha: fallback local