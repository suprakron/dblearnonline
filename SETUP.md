# คู่มือติดตั้งโปรเจกต์ DBLearn Online บน Windows

## สิ่งที่ต้องโหลดก่อน

### 1. Python 3.11 (แนะนำ) หรือ 3.9+
- ไปที่ https://www.python.org/downloads/
- กด **Download Python 3.11.x** (ตัวล่าสุด)
- ติดตั้ง → **ติ๊ก ✅ "Add Python to PATH"** ให้แน่ใจก่อนกด Install Now

ตรวจสอบว่าติดตั้งสำเร็จ เปิด Command Prompt แล้วพิมพ์:
```
python --version
```
ต้องขึ้น `Python 3.11.x` หรือใกล้เคียง

---

## วิธีย้ายโปรเจกต์จากเครื่อง Mac มา Windows

เนื่องจากไม่มี GitHub ให้ **copy โฟลเดอร์ `dblearnonline`** ทั้งหมดผ่าน USB หรือ Google Drive
**ยกเว้น** โฟลเดอร์เหล่านี้ไม่ต้องเอามา (ไฟล์ Mac-specific):
- โฟลเดอร์ `env/` (สร้างใหม่บน Windows)
- ไฟล์ `__pycache__/` ทุกอัน

โครงสร้างที่ต้องเอามา:
```
dblearnonline/
├── appdblearn/
│   ├── static/
│   ├── templates/
│   ├── migrations/
│   ├── views.py
│   ├── urls.py
│   ├── models.py
│   └── apps.py
├── dblearnonline/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── db.sqlite3
└── requirements.txt
```

---

## ขั้นตอนติดตั้งบน Windows

### ขั้นตอนที่ 1 — เปิด Command Prompt (cmd)
กด `Win + R` พิมพ์ `cmd` แล้วกด Enter

### ขั้นตอนที่ 2 — เข้าไปในโฟลเดอร์โปรเจกต์
```cmd
cd C:\Users\ชื่อuser\Desktop\dblearnonline
```
> เปลี่ยน `ชื่อuser` ให้ตรงกับเครื่องตัวเอง เช่น `cd C:\Users\Student\Desktop\dblearnonline`

### ขั้นตอนที่ 3 — สร้าง Virtual Environment
```cmd
python -m venv env
```
จะมีโฟลเดอร์ `env` สร้างขึ้นมาในโฟลเดอร์โปรเจกต์

### ขั้นตอนที่ 4 — เปิดใช้งาน Virtual Environment
```cmd
env\Scripts\activate
```
ถ้าสำเร็จจะเห็น `(env)` ขึ้นที่หน้า prompt เช่น:
```
(env) C:\Users\Student\Desktop\dblearnonline>
```

> **ถ้า error ว่า "cannot be loaded because running scripts is disabled":**
> ให้เปิด PowerShell แบบ Administrator แล้วพิมพ์:
> ```
> Set-ExecutionPolicy RemoteSigned
> ```
> แล้วพิมพ์ `Y` กด Enter จากนั้นกลับมา cmd ทำขั้นตอนที่ 4 ใหม่

### ขั้นตอนที่ 5 — ติดตั้ง packages ทั้งหมด
```cmd
pip install -r requirements.txt
```
รอสักครู่จนติดตั้งเสร็จทุกตัว

### ขั้นตอนที่ 6 — สร้างฐานข้อมูล
```cmd
python manage.py migrate
```

### ขั้นตอนที่ 7 — รันเซิร์ฟเวอร์
```cmd
python manage.py runserver
```
จะขึ้นข้อความแบบนี้:
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

### ขั้นตอนที่ 8 — เปิดเว็บไซต์
เปิด Browser แล้วไปที่:
```
http://127.0.0.1:8000
```

---

## หน้าทั้งหมดในโปรเจกต์

| หน้า | URL |
|------|-----|
| หน้าแรก | http://127.0.0.1:8000/ |
| เข้าสู่ระบบ | http://127.0.0.1:8000/login/ |
| สมัครสมาชิก | http://127.0.0.1:8000/register/ |
| คำอธิบายรายวิชา | http://127.0.0.1:8000/course_description/ |
| บทเรียน (วิดีโอ Ep.7) | http://127.0.0.1:8000/lesson_detail/ |
| แบบทดสอบก่อนเรียน | http://127.0.0.1:8000/pretest/ |
| แบบทดสอบหลังเรียน | http://127.0.0.1:8000/posttest/ |
| ผลการเรียน | http://127.0.0.1:8000/results/ |
| Teacher Dashboard | http://127.0.0.1:8000/teacher/ |

---

## ครั้งต่อไปที่จะรันโปรเจกต์

เปิด cmd แล้วพิมพ์ทีละบรรทัด:
```cmd
cd C:\Users\ชื่อuser\Desktop\dblearnonline
env\Scripts\activate
python manage.py runserver
```

---

## แก้ปัญหาที่พบบ่อย

**ปัญหา:** `python` ไม่รู้จัก
**แก้:** ติดตั้ง Python ใหม่และติ๊ก "Add Python to PATH"

**ปัญหา:** `pip install` ช้ามาก หรือ timeout
**แก้:** เปลี่ยน mirror เป็นของไทย:
```cmd
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

**ปัญหา:** Port 8000 ถูกใช้งานอยู่แล้ว
**แก้:** เปลี่ยน port:
```cmd
python manage.py runserver 8080
```
แล้วเปิด http://127.0.0.1:8080

**ปัญหา:** หน้าเว็บแสดงผิด / CSS ไม่โหลด
**แก้:** กด `Ctrl + Shift + R` เพื่อ hard refresh ใน browser

**ปัญหา:** `No module named 'django'`
**แก้:** ตรวจสอบว่า activate env แล้ว ต้องเห็น `(env)` อยู่หน้า prompt

---

## โครงสร้าง packages ที่ใช้

| Package | เวอร์ชัน | หน้าที่ |
|---------|---------|--------|
| Django | 4.2.30 | Web framework หลัก |
| asgiref | 3.11.1 | ASGI support |
| sqlparse | 0.5.5 | SQL formatter (Django ใช้) |
| pillow | 11.3.0 | จัดการรูปภาพ |
| typing_extensions | 4.15.0 | Type hints |
