import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie

def home(request):
    return render(request, 'dblearn/index.html')

def register(request):
    return render(request, 'dblearn/register.html')

def course_description(request):
    return render(request, 'dblearn/course_description.html')

@ensure_csrf_cookie
def lesson_detail(request):
    return render(request, 'dblearn/lesson_detail.html')

@require_POST
def chatbot_mock_reply(request):
    try:
        data = json.loads(request.body)
        message = data.get("message", "").strip().lower()
    except json.JSONDecodeError:
        return JsonResponse({"reply": "รูปแบบข้อมูลไม่ถูกต้อง"}, status=400)

    if "บทที่ 1" in message:
        reply = """
        <strong>สรุปบทที่ 1</strong><br>
        บทนี้อธิบายความหมายของฐานข้อมูล ความสำคัญ และองค์ประกอบพื้นฐาน
        เช่น ตาราง ฟิลด์ และระเบียน
        """
    elif "ก่อนเรียน" in message or "pretest" in message:
        reply = """
        <strong>แบบทดสอบก่อนเรียน</strong><br>
        มีจำนวน 10 ข้อ ใช้วัดความรู้พื้นฐานก่อนเริ่มเรียน
        """
    elif "หลังเรียน" in message or "posttest" in message:
        reply = """
        <strong>แบบทดสอบหลังเรียน</strong><br>
        มีจำนวน 20 ข้อ ใช้ประเมินผลหลังเรียนจบหน่วย
        """
    elif "คะแนน" in message or "ผลการเรียน" in message:
        reply = """
        <strong>ผลการเรียน (ตัวอย่าง)</strong><br>
        เรียนแล้ว 2/10 บท<br>
        คะแนนสะสม 18/30
        """
    elif "ครู" in message or "ผู้สอน" in message:
        reply = """
        <strong>ข้อมูลผู้สอน</strong><br>
        ชื่อ: ครูผู้สอนวิชาฐานข้อมูล<br>
        เวลาติดต่อ: วันจันทร์ - ศุกร์ 08:30 - 16:30
        """
    elif "บทเรียน" in message or "lesson" in message:
        reply = """
        <strong>ข้อมูลบทเรียน</strong><br>
        ขณะนี้มีบทเรียนตัวอย่างในระบบ เช่น<br>
        1. บทที่ 1 ความรู้เบื้องต้นเกี่ยวกับฐานข้อมูล<br>
        2. บทที่ 2 การออกแบบตารางข้อมูล<br>
        3. บทที่ 3 ความสัมพันธ์ระหว่างตาราง
        """
    else:
        reply = """
        ขอโทษครับ ตอนนี้ผมยังเป็น <strong>mock chatbot</strong><br>
        ลองพิมพ์คำถาม เช่น<br>
        • บทเรียน<br>
        • สรุปบทที่ 1<br>
        • แบบทดสอบก่อนเรียน<br>
        • คะแนน<br>
        • ผู้สอน
        """

    return JsonResponse({"reply": reply})

def pretest(request):
    return render(request, 'dblearn/pretest.html')

def posttest(request):
    return render(request, 'dblearn/posttest.html')

def results(request):
    return render(request, 'dblearn/results.html')

def teacher_dashboard(request):
    return render(request, 'dblearn/teacher_dashboard.html')

def login_page(request):
    return render(request, 'dblearn/login.html')

def exercise(request):
    return render(request, 'dblearn/exercise.html')

