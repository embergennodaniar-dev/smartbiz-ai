"""
Ishga tushirish: python clean_demo_data.py
Eski demo ma'lumotlarni (user_id=NULL) avtomatik tozalaydi.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from models.database import SessionLocal, Store, init_db

def clean():
    init_db()
    db = SessionLocal()
    try:
        orphans = db.query(Store).filter(Store.user_id == None).all()
        if not orphans:
            print("OK - tozalash kerak emas.")
            return
        
        for store in orphans:
            print(f"O'chirildi: ID:{store.id} '{store.name}'")
            db.delete(store)
        
        db.commit()
        print(f"Jami {len(orphans)} ta eski do'kon o'chirildi!")
    finally:
        db.close()

if __name__ == "__main__":
    clean()
