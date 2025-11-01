from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import Product, Client, Invoice, InvoiceItem, User
from schemas import ProductSchema, ClientSchema, InvoiceSchema, UserSchema, LoginSchema
from passlib.hash import bcrypt

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Sunu ERP API", version="1.0")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "✅ Sunu ERP Backend Running"}


# -------------------- PRODUCTS --------------------
@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()

@app.post("/products")
def add_product(product: ProductSchema, db: Session = Depends(get_db)):
    new_product = Product(name=product.name, price=product.price)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


# -------------------- CLIENTS --------------------
@app.get("/clients")
def get_clients(db: Session = Depends(get_db)):
    return db.query(Client).all()

@app.post("/clients")
def add_client(client: ClientSchema, db: Session = Depends(get_db)):
    new_client = Client(name=client.name, email=client.email, phone=client.phone)
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return new_client


# -------------------- INVOICES --------------------
@app.get("/invoices")
def get_invoices(db: Session = Depends(get_db)):
    return db.query(Invoice).all()

@app.post("/invoices")
def create_invoice(data: InvoiceSchema, db: Session = Depends(get_db)):
    invoice = Invoice(client_id=data.client_id, total=0)
    db.add(invoice)
    db.commit()
    db.refresh(invoice)

    total = 0
    for item in data.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Produit introuvable")

        line_total = product.price * item.quantity
        db.add(InvoiceItem(invoice_id=invoice.id, product_id=item.product_id, quantity=item.quantity, total=line_total))
        total += line_total

    invoice.total = total
    db.commit()
    return {"invoice_id": invoice.id, "total": total}


# -------------------- AUTH --------------------
@app.post("/register")
def register(user: UserSchema, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email déjà utilisé")

    hashed = bcrypt.hash(user.password)
    new_user = User(name=user.name, email=user.email, password=hashed)
    db.add(new_user)
    db.commit()
    return {"message": "Utilisateur créé ✅"}

@app.post("/login")
def login(user: LoginSchema, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not bcrypt.verify(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Identifiants invalides ❌")

    return {"message": "Connexion réussie ✅", "user": db_user.name}
