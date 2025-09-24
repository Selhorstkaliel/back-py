def calcular_desconto_efetivo(db, user):
    # Lógica: vendedor -> seller.seller_discount, representante -> default_discount, admin -> 0 ou payload
    if user["role"] == "vendedor":
        s = db.execute("SELECT seller_discount FROM sellers WHERE user_id=?", (user["id"],)).fetchone()
        return float(s[0]) if s else 0.0
    elif user["role"] == "representante":
        r = db.execute("SELECT default_discount FROM representatives WHERE user_id=?", (user["id"],)).fetchone()
        return float(r[0]) if r else 0.0
    return 0.0