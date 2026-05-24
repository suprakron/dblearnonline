from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="วันที่สร้าง")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="วันที่แก้ไข")

    class Meta:
        abstract = True


class ActiveStatusChoices(models.TextChoices):
    ACTIVE = "active", "ใช้งาน"
    INACTIVE = "inactive", "ไม่ใช้งาน"
    SUSPENDED = "suspended", "ระงับการใช้งาน"


class UserRoleChoices(models.TextChoices):
    STUDENT = "student", "นักเรียน"
    TEACHER = "teacher", "ครู"
    ADMIN = "admin", "ผู้ดูแลระบบ"


class PublishStatusChoices(models.TextChoices):
    DRAFT = "draft", "ฉบับร่าง"
    PUBLISHED = "published", "เผยแพร่"
    HIDDEN = "hidden", "ซ่อน"


class GenderChoices(models.TextChoices):
    MALE = "male", "ชาย"
    FEMALE = "female", "หญิง"
    OTHER = "other", "อื่น ๆ"


class MenuTypeChoices(models.TextChoices):
    MAIN = "main", "เมนูหลัก"
    SUB = "sub", "เมนูย่อย"


class QuizTypeChoices(models.TextChoices):
    PRETEST = "pretest", "ก่อนเรียน"
    POSTTEST = "posttest", "หลังเรียน"
    PRACTICE = "practice", "แบบฝึกทบทวน"


class AttemptStatusChoices(models.TextChoices):
    IN_PROGRESS = "in_progress", "กำลังทำ"
    SUBMITTED = "submitted", "ส่งแล้ว"
    TIMEOUT = "timeout", "หมดเวลา"
    CANCELLED = "cancelled", "ยกเลิก"


class LessonProgressChoices(models.TextChoices):
    NOT_STARTED = "not_started", "ยังไม่เรียน"
    IN_PROGRESS = "in_progress", "กำลังเรียน"
    COMPLETED = "completed", "เรียนจบ"


class CommentStatusChoices(models.TextChoices):
    PENDING = "pending", "รออนุมัติ"
    APPROVED = "approved", "อนุมัติ"
    HIDDEN = "hidden", "ซ่อน"


class ReviewStatusChoices(models.TextChoices):
    PENDING = "pending", "รอตรวจ"
    CHECKED = "checked", "ตรวจแล้ว"
    RETURNED = "returned", "ส่งกลับ"


class AlertRiskLevelChoices(models.TextChoices):
    LOW = "low", "ต่ำ"
    MEDIUM = "medium", "ปานกลาง"
    HIGH = "high", "สูง"
    CRITICAL = "critical", "วิกฤต"


class AlertReviewStatusChoices(models.TextChoices):
    NEW = "new", "ใหม่"
    REVIEWING = "reviewing", "กำลังตรวจสอบ"
    RESOLVED = "resolved", "ตรวจสอบแล้ว"


class QuestionTypeChoices(models.TextChoices):
    MULTIPLE_CHOICE = "multiple_choice", "ปรนัย"
    TRUE_FALSE = "true_false", "ถูกผิด"
    SHORT_ANSWER = "short_answer", "คำตอบสั้น"


class CustomUser(AbstractUser):
    prefix = models.CharField(max_length=20, blank=True, verbose_name="คำนำหน้า")
    display_name = models.CharField(max_length=150, blank=True, verbose_name="ชื่อที่แสดง")
    phone = models.CharField(max_length=20, blank=True, verbose_name="เบอร์โทร")
    profile_image = models.ImageField(upload_to="profiles/", blank=True, null=True, verbose_name="รูปโปรไฟล์")
    role = models.CharField(
        max_length=20,
        choices=UserRoleChoices.choices,
        default=UserRoleChoices.STUDENT,
        verbose_name="บทบาทผู้ใช้",
    )
    status = models.CharField(
        max_length=20,
        choices=ActiveStatusChoices.choices,
        default=ActiveStatusChoices.ACTIVE,
        verbose_name="สถานะการใช้งาน",
    )

    def __str__(self) -> str:
        return self.display_name or self.get_full_name() or self.username


class StudentProfile(TimeStampedModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="student_profile",
        verbose_name="ผู้ใช้",
    )
    student_code = models.CharField(max_length=50, unique=True, verbose_name="รหัสนักเรียน")
    education_level = models.CharField(max_length=50, blank=True, verbose_name="ระดับชั้น")
    class_room = models.CharField(max_length=50, blank=True, verbose_name="ห้อง")
    department = models.CharField(max_length=100, blank=True, verbose_name="สาขาวิชา")
    academic_year = models.CharField(max_length=20, blank=True, verbose_name="ปีการศึกษา")
    student_number = models.CharField(max_length=20, blank=True, verbose_name="เลขที่")
    birth_date = models.DateField(blank=True, null=True, verbose_name="วันเกิด")
    gender = models.CharField(
        max_length=20,
        choices=GenderChoices.choices,
        blank=True,
        verbose_name="เพศ",
    )
    guardian_phone = models.CharField(max_length=20, blank=True, verbose_name="เบอร์ผู้ปกครอง/ฉุกเฉิน")

    class Meta:
        verbose_name = "ข้อมูลนักเรียน"
        verbose_name_plural = "ข้อมูลนักเรียน"

    def __str__(self) -> str:
        return f"{self.student_code} - {self.user}"


class TeacherProfile(TimeStampedModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="teacher_profile",
        verbose_name="ผู้ใช้",
    )
    teacher_name = models.CharField(max_length=255, verbose_name="ชื่อ-นามสกุล")
    position = models.CharField(max_length=100, blank=True, verbose_name="ตำแหน่ง")
    department = models.CharField(max_length=100, blank=True, verbose_name="แผนกวิชา")
    teacher_image = models.ImageField(upload_to="teachers/", blank=True, null=True, verbose_name="รูปภาพ")
    contact_info = models.TextField(blank=True, verbose_name="ช่องทางติดต่อ")
    facebook_url = models.URLField(blank=True, verbose_name="Facebook")
    line_id = models.CharField(max_length=100, blank=True, verbose_name="Line")
    email_contact = models.EmailField(blank=True, verbose_name="Email ติดต่อ")
    website_url = models.URLField(blank=True, verbose_name="เว็บไซต์")

    class Meta:
        verbose_name = "ข้อมูลครู"
        verbose_name_plural = "ข้อมูลครู"

    def __str__(self) -> str:
        return self.teacher_name


class Course(TimeStampedModel):
    course_code = models.CharField(max_length=50, unique=True, verbose_name="รหัสวิชา")
    course_name = models.CharField(max_length=255, verbose_name="ชื่อวิชา")
    course_description = models.TextField(blank=True, verbose_name="คำอธิบายรายวิชา")
    course_objective = models.TextField(blank=True, verbose_name="วัตถุประสงค์รายวิชา")
    total_hours = models.PositiveIntegerField(default=0, verbose_name="จำนวนชั่วโมง")
    credit_unit = models.DecimalField(max_digits=4, decimal_places=1, default=0, verbose_name="หน่วยกิต")
    cover_image = models.ImageField(upload_to="courses/", blank=True, null=True, verbose_name="รูปปกวิชา")
    main_teacher = models.ForeignKey(
        TeacherProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="courses",
        verbose_name="ผู้สอนหลัก",
    )
    publish_status = models.CharField(
        max_length=20,
        choices=PublishStatusChoices.choices,
        default=PublishStatusChoices.DRAFT,
        verbose_name="สถานะเผยแพร่",
    )

    class Meta:
        verbose_name = "รายวิชา"
        verbose_name_plural = "รายวิชา"
        ordering = ["course_code"]

    def __str__(self) -> str:
        return f"{self.course_code} - {self.course_name}"


class Menu(TimeStampedModel):
    menu_name = models.CharField(max_length=100, verbose_name="ชื่อเมนู")
    menu_type = models.CharField(
        max_length=10,
        choices=MenuTypeChoices.choices,
        default=MenuTypeChoices.MAIN,
        verbose_name="ประเภทเมนู",
    )
    parent_menu = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
        verbose_name="เมนูแม่",
    )
    display_order = models.PositiveIntegerField(default=0, verbose_name="ลำดับการแสดงผล")
    menu_path = models.CharField(max_length=255, blank=True, verbose_name="path/url")
    menu_icon = models.CharField(max_length=100, blank=True, verbose_name="icon")
    permission_role = models.CharField(max_length=20, blank=True, verbose_name="สิทธิ์การเข้าถึง")
    menu_status = models.CharField(
        max_length=20,
        choices=PublishStatusChoices.choices,
        default=PublishStatusChoices.PUBLISHED,
        verbose_name="สถานะการใช้งาน",
    )

    class Meta:
        verbose_name = "เมนู"
        verbose_name_plural = "เมนู"
        ordering = ["display_order", "id"]

    def __str__(self) -> str:
        return self.menu_name


class Banner(TimeStampedModel):
    banner_name = models.CharField(max_length=255, verbose_name="ชื่อแบนเนอร์")
    banner_title = models.CharField(max_length=255, verbose_name="หัวข้อ")
    banner_description = models.TextField(blank=True, verbose_name="รายละเอียด")
    banner_image = models.ImageField(upload_to="banners/", verbose_name="รูปภาพ")
    button_text = models.CharField(max_length=100, blank=True, verbose_name="ข้อความปุ่ม")
    button_link = models.URLField(blank=True, verbose_name="ลิงก์ปลายทาง")
    display_order = models.PositiveIntegerField(default=0, verbose_name="ลำดับการแสดง")
    start_date = models.DateTimeField(blank=True, null=True, verbose_name="วันที่เริ่มแสดง")
    end_date = models.DateTimeField(blank=True, null=True, verbose_name="วันที่สิ้นสุด")
    publish_status = models.CharField(
        max_length=20,
        choices=PublishStatusChoices.choices,
        default=PublishStatusChoices.DRAFT,
        verbose_name="สถานะเผยแพร่",
    )

    class Meta:
        verbose_name = "แบนเนอร์"
        verbose_name_plural = "แบนเนอร์"
        ordering = ["display_order", "-created_at"]

    def __str__(self) -> str:
        return self.banner_name


class Lesson(TimeStampedModel):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="lessons",
        verbose_name="รายวิชา",
    )
    lesson_no = models.PositiveIntegerField(verbose_name="ลำดับบทเรียน")
    lesson_title = models.CharField(max_length=255, verbose_name="ชื่อบทเรียน")
    lesson_description = models.TextField(blank=True, verbose_name="คำอธิบายบทเรียน")
    lesson_content = models.TextField(blank=True, verbose_name="เนื้อหาหลัก")
    thumbnail_image = models.ImageField(upload_to="lessons/thumbnails/", blank=True, null=True, verbose_name="รูปปก")
    video_url = models.URLField(blank=True, verbose_name="ลิงก์วิดีโอ")
    attachment_info = models.TextField(blank=True, verbose_name="ข้อมูลไฟล์เอกสารประกอบ")
    display_order = models.PositiveIntegerField(default=0, verbose_name="ลำดับการแสดง")
    study_duration = models.PositiveIntegerField(default=0, verbose_name="ระยะเวลาเรียน (นาที)")
    publish_status = models.CharField(
        max_length=20,
        choices=PublishStatusChoices.choices,
        default=PublishStatusChoices.DRAFT,
        verbose_name="สถานะเผยแพร่",
    )

    class Meta:
        verbose_name = "บทเรียน"
        verbose_name_plural = "บทเรียน"
        ordering = ["course", "lesson_no"]
        unique_together = ("course", "lesson_no")

    def __str__(self) -> str:
        return f"{self.course.course_code} - บทที่ {self.lesson_no} {self.lesson_title}"


class LessonFile(TimeStampedModel):
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="files",
        verbose_name="บทเรียน",
    )
    file_name = models.CharField(max_length=255, verbose_name="ชื่อไฟล์")
    file_type = models.CharField(max_length=50, blank=True, verbose_name="ชนิดไฟล์")
    file = models.FileField(upload_to="lesson_files/", verbose_name="ไฟล์")
    file_size = models.PositiveBigIntegerField(default=0, verbose_name="ขนาดไฟล์ (bytes)")
    file_description = models.TextField(blank=True, verbose_name="คำอธิบายไฟล์")
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="uploaded_lesson_files",
        verbose_name="ผู้อัปโหลด",
    )

    class Meta:
        verbose_name = "ไฟล์บทเรียน"
        verbose_name_plural = "ไฟล์บทเรียน"

    def __str__(self) -> str:
        return self.file_name


class LessonComment(TimeStampedModel):
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="บทเรียน",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="lesson_comments",
        verbose_name="ผู้แสดงความคิดเห็น",
    )
    comment_text = models.TextField(verbose_name="ข้อความคอมเมนต์")
    comment_status = models.CharField(
        max_length=20,
        choices=CommentStatusChoices.choices,
        default=CommentStatusChoices.PENDING,
        verbose_name="สถานะคอมเมนต์",
    )
    parent_comment = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="replies",
        verbose_name="คอมเมนต์แม่",
    )

    class Meta:
        verbose_name = "คอมเมนต์บทเรียน"
        verbose_name_plural = "คอมเมนต์บทเรียน"
        ordering = ["created_at"]

    def __str__(self) -> str:
        return f"Comment by {self.user} on {self.lesson}"


class Exercise(TimeStampedModel):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="exercises",
        verbose_name="รายวิชา",
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="exercises",
        verbose_name="บทเรียน",
    )
    exercise_title = models.CharField(max_length=255, verbose_name="ชื่อแบบฝึกหัด")
    instruction = models.TextField(blank=True, verbose_name="คำชี้แจง")
    full_score = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name="คะแนนเต็ม")
    start_date = models.DateTimeField(blank=True, null=True, verbose_name="วันเริ่ม")
    end_date = models.DateTimeField(blank=True, null=True, verbose_name="วันสิ้นสุด")
    attachment_file = models.FileField(upload_to="exercise_attachments/", blank=True, null=True, verbose_name="ไฟล์แนบ")
    publish_status = models.CharField(
        max_length=20,
        choices=PublishStatusChoices.choices,
        default=PublishStatusChoices.DRAFT,
        verbose_name="สถานะเผยแพร่",
    )

    class Meta:
        verbose_name = "แบบฝึกหัด"
        verbose_name_plural = "แบบฝึกหัด"

    def __str__(self) -> str:
        return self.exercise_title


class ExerciseSubmission(TimeStampedModel):
    exercise = models.ForeignKey(
        Exercise,
        on_delete=models.CASCADE,
        related_name="submissions",
        verbose_name="แบบฝึกหัด",
    )
    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name="exercise_submissions",
        verbose_name="นักเรียน",
    )
    answer_text = models.TextField(blank=True, verbose_name="ข้อความคำตอบ")
    submission_file = models.FileField(upload_to="exercise_submissions/", blank=True, null=True, verbose_name="ไฟล์ที่ส่ง")
    submitted_at = models.DateTimeField(blank=True, null=True, verbose_name="วันที่ส่ง")
    score_received = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name="คะแนนที่ได้")
    teacher_feedback = models.TextField(blank=True, verbose_name="ความเห็นจากครู")
    review_status = models.CharField(
        max_length=20,
        choices=ReviewStatusChoices.choices,
        default=ReviewStatusChoices.PENDING,
        verbose_name="สถานะการตรวจ",
    )

    class Meta:
        verbose_name = "การส่งแบบฝึกหัด"
        verbose_name_plural = "การส่งแบบฝึกหัด"

    def __str__(self) -> str:
        return f"{self.student} - {self.exercise}"


class Quiz(TimeStampedModel):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="quizzes",
        verbose_name="รายวิชา",
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="quizzes",
        verbose_name="บทเรียน",
    )
    quiz_title = models.CharField(max_length=255, verbose_name="ชื่อแบบทดสอบ")
    quiz_type = models.CharField(
        max_length=20,
        choices=QuizTypeChoices.choices,
        default=QuizTypeChoices.PRETEST,
        verbose_name="ประเภทแบบทดสอบ",
    )
    quiz_description = models.TextField(blank=True, verbose_name="คำอธิบาย")
    question_count = models.PositiveIntegerField(default=0, verbose_name="จำนวนข้อ")
    full_score = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name="คะแนนเต็ม")
    time_limit = models.PositiveIntegerField(default=0, verbose_name="เวลาที่กำหนด (นาที)")
    shuffle_questions = models.BooleanField(default=False, verbose_name="สุ่มข้อสอบ")
    shuffle_choices = models.BooleanField(default=False, verbose_name="สุ่มตัวเลือก")
    show_result_immediately = models.BooleanField(default=False, verbose_name="แสดงผลคะแนนทันที")
    publish_status = models.CharField(
        max_length=20,
        choices=PublishStatusChoices.choices,
        default=PublishStatusChoices.DRAFT,
        verbose_name="สถานะเผยแพร่",
    )

    class Meta:
        verbose_name = "แบบทดสอบ"
        verbose_name_plural = "แบบทดสอบ"

    def __str__(self) -> str:
        return self.quiz_title


class Question(TimeStampedModel):
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name="questions",
        verbose_name="แบบทดสอบ",
    )
    question_no = models.PositiveIntegerField(verbose_name="เลขข้อ")
    question_text = models.TextField(verbose_name="คำถาม")
    question_image = models.ImageField(upload_to="questions/", blank=True, null=True, verbose_name="รูปภาพประกอบ")
    question_type = models.CharField(
        max_length=30,
        choices=QuestionTypeChoices.choices,
        default=QuestionTypeChoices.MULTIPLE_CHOICE,
        verbose_name="ประเภทคำถาม",
    )
    question_score = models.DecimalField(max_digits=6, decimal_places=2, default=1, verbose_name="คะแนน")
    difficulty_level = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="ระดับความยาก",
    )
    explanation_text = models.TextField(blank=True, verbose_name="คำอธิบายเฉลย")

    class Meta:
        verbose_name = "ข้อคำถาม"
        verbose_name_plural = "ข้อคำถาม"
        ordering = ["quiz", "question_no"]
        unique_together = ("quiz", "question_no")

    def __str__(self) -> str:
        return f"{self.quiz} - ข้อ {self.question_no}"


class Choice(TimeStampedModel):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="choices",
        verbose_name="คำถาม",
    )
    choice_label = models.CharField(max_length=5, verbose_name="ตัวเลือก")
    choice_text = models.TextField(verbose_name="ข้อความตัวเลือก")
    is_correct = models.BooleanField(default=False, verbose_name="ถูกต้อง")
    display_order = models.PositiveIntegerField(default=0, verbose_name="ลำดับตัวเลือก")

    class Meta:
        verbose_name = "ตัวเลือกคำตอบ"
        verbose_name_plural = "ตัวเลือกคำตอบ"
        ordering = ["question", "display_order"]

    def __str__(self) -> str:
        return f"{self.question} - {self.choice_label}"


class QuizAttempt(TimeStampedModel):
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name="attempts",
        verbose_name="แบบทดสอบ",
    )
    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name="quiz_attempts",
        verbose_name="นักเรียน",
    )
    start_time = models.DateTimeField(verbose_name="เวลาเริ่ม")
    submit_time = models.DateTimeField(blank=True, null=True, verbose_name="เวลาส่ง")
    time_used = models.PositiveIntegerField(default=0, verbose_name="เวลาที่ใช้ (วินาที)")
    score_received = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name="คะแนนที่ได้")
    score_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="เปอร์เซ็นต์คะแนน")
    attempt_status = models.CharField(
        max_length=20,
        choices=AttemptStatusChoices.choices,
        default=AttemptStatusChoices.IN_PROGRESS,
        verbose_name="สถานะการทำข้อสอบ",
    )
    answered_count = models.PositiveIntegerField(default=0, verbose_name="จำนวนข้อที่ตอบแล้ว")
    unanswered_count = models.PositiveIntegerField(default=0, verbose_name="จำนวนข้อที่ยังไม่ตอบ")

    class Meta:
        verbose_name = "การทำแบบทดสอบ"
        verbose_name_plural = "การทำแบบทดสอบ"

    def __str__(self) -> str:
        return f"{self.student} - {self.quiz}"


class StudentAnswer(TimeStampedModel):
    attempt = models.ForeignKey(
        QuizAttempt,
        on_delete=models.CASCADE,
        related_name="answers",
        verbose_name="การทำแบบทดสอบ",
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="student_answers",
        verbose_name="คำถาม",
    )
    choice = models.ForeignKey(
        Choice,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="selected_answers",
        verbose_name="ตัวเลือกที่เลือก",
    )
    is_correct = models.BooleanField(default=False, verbose_name="ตอบถูก")
    answer_score = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name="คะแนนที่ได้")
    answered_at = models.DateTimeField(blank=True, null=True, verbose_name="เวลาที่ตอบ")
    answer_order = models.PositiveIntegerField(default=0, verbose_name="ลำดับการตอบ")

    class Meta:
        verbose_name = "คำตอบของนักเรียน"
        verbose_name_plural = "คำตอบของนักเรียน"

    def __str__(self) -> str:
        return f"{self.attempt} - {self.question}"


class LearningProgress(TimeStampedModel):
    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name="learning_progress",
        verbose_name="นักเรียน",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="learning_progress",
        verbose_name="รายวิชา",
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="learning_progress",
        verbose_name="บทเรียน",
    )
    lesson_status = models.CharField(
        max_length=20,
        choices=LessonProgressChoices.choices,
        default=LessonProgressChoices.NOT_STARTED,
        verbose_name="สถานะบทเรียน",
    )
    progress_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="เปอร์เซ็นต์ความคืบหน้า")
    started_at = models.DateTimeField(blank=True, null=True, verbose_name="วันที่เริ่มเรียน")
    completed_at = models.DateTimeField(blank=True, null=True, verbose_name="วันที่เรียนจบ")
    study_time_total = models.PositiveIntegerField(default=0, verbose_name="เวลาเรียนสะสม (วินาที)")

    class Meta:
        verbose_name = "ความคืบหน้าการเรียน"
        verbose_name_plural = "ความคืบหน้าการเรียน"
        unique_together = ("student", "course", "lesson")

    def __str__(self) -> str:
        return f"{self.student} - {self.lesson}"


class GradeSummary(TimeStampedModel):
    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name="grade_summaries",
        verbose_name="นักเรียน",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="grade_summaries",
        verbose_name="รายวิชา",
    )
    pretest_score = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name="คะแนนก่อนเรียน")
    posttest_score = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name="คะแนนหลังเรียน")
    exercise_score = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name="คะแนนแบบฝึกหัด")
    total_score = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name="คะแนนรวม")
    grade_level = models.CharField(max_length=10, blank=True, verbose_name="ระดับผลการเรียน")

    class Meta:
        verbose_name = "สรุปผลคะแนน"
        verbose_name_plural = "สรุปผลคะแนน"
        unique_together = ("student", "course")

    def __str__(self) -> str:
        return f"{self.student} - {self.course}"


class VisitStat(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="visit_stats",
        verbose_name="ผู้ใช้",
    )
    visitor_id = models.CharField(max_length=100, blank=True, verbose_name="รหัสผู้เยี่ยมชม")
    visited_at = models.DateTimeField(auto_now_add=True, verbose_name="วันที่เวลาเข้าชม")
    page_url = models.CharField(max_length=255, verbose_name="หน้าเว็บ")
    ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name="IP Address")
    browser_name = models.CharField(max_length=100, blank=True, verbose_name="Browser")
    device_type = models.CharField(max_length=100, blank=True, verbose_name="อุปกรณ์")
    session_id = models.CharField(max_length=255, blank=True, verbose_name="Session ID")
    duration_seconds = models.PositiveIntegerField(default=0, verbose_name="ระยะเวลา (วินาที)")

    class Meta:
        verbose_name = "สถิติการเข้าชม"
        verbose_name_plural = "สถิติการเข้าชม"

    def __str__(self) -> str:
        return f"{self.page_url} - {self.visited_at}"


class ChatbotLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="chatbot_logs",
        verbose_name="ผู้ใช้",
    )
    session_id = models.CharField(max_length=255, blank=True, verbose_name="Session ID")
    question_text = models.TextField(verbose_name="คำถาม")
    answer_text = models.TextField(verbose_name="คำตอบ")
    chat_time = models.DateTimeField(auto_now_add=True, verbose_name="วันที่เวลา")
    page_name = models.CharField(max_length=255, blank=True, verbose_name="หน้าที่ถาม")
    question_type = models.CharField(max_length=100, blank=True, verbose_name="ประเภทคำถาม")

    class Meta:
        verbose_name = "ประวัติ Chatbot"
        verbose_name_plural = "ประวัติ Chatbot"
        ordering = ["-chat_time"]

    def __str__(self) -> str:
        return f"{self.user} - {self.chat_time}"


class ExamAlert(models.Model):
    attempt = models.ForeignKey(
        QuizAttempt,
        on_delete=models.CASCADE,
        related_name="alerts",
        verbose_name="การทำข้อสอบ",
    )
    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name="exam_alerts",
        verbose_name="นักเรียน",
    )
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name="alerts",
        verbose_name="แบบทดสอบ",
    )
    alert_type = models.CharField(max_length=100, verbose_name="ประเภทความผิดปกติ")
    alert_detail = models.TextField(blank=True, verbose_name="รายละเอียดเหตุการณ์")
    alert_time = models.DateTimeField(auto_now_add=True, verbose_name="เวลาเกิดเหตุ")
    risk_level = models.CharField(
        max_length=20,
        choices=AlertRiskLevelChoices.choices,
        default=AlertRiskLevelChoices.LOW,
        verbose_name="ระดับความเสี่ยง",
    )
    review_status = models.CharField(
        max_length=20,
        choices=AlertReviewStatusChoices.choices,
        default=AlertReviewStatusChoices.NEW,
        verbose_name="สถานะตรวจสอบ",
    )
    admin_note = models.TextField(blank=True, verbose_name="หมายเหตุจากแอดมิน")

    class Meta:
        verbose_name = "แจ้งเตือนทุจริต"
        verbose_name_plural = "แจ้งเตือนทุจริต"
        ordering = ["-alert_time"]

    def __str__(self) -> str:
        return f"{self.student} - {self.alert_type}"


class SystemSetting(models.Model):
    site_name = models.CharField(max_length=255, default="DB Learning Online", verbose_name="ชื่อเว็บไซต์")
    site_logo = models.ImageField(upload_to="settings/", blank=True, null=True, verbose_name="โลโก้")
    footer_text = models.CharField(max_length=255, blank=True, verbose_name="ข้อความส่วนท้าย")
    theme_color = models.CharField(max_length=20, blank=True, verbose_name="สีธีม")
    chatbot_enabled = models.BooleanField(default=True, verbose_name="เปิดใช้งาน Chatbot")
    registration_enabled = models.BooleanField(default=True, verbose_name="เปิดสมัครสมาชิก")
    quiz_attempt_limit = models.PositiveIntegerField(default=1, verbose_name="จำนวนครั้งที่อนุญาตให้สอบ")
    session_timeout = models.PositiveIntegerField(default=30, verbose_name="เวลาหมด Session (นาที)")
    copyright_year = models.PositiveIntegerField(default=2026, verbose_name="ปีลิขสิทธิ์")

    class Meta:
        verbose_name = "การตั้งค่าระบบ"
        verbose_name_plural = "การตั้งค่าระบบ"

    def __str__(self) -> str:
        return self.site_name


class Announcement(TimeStampedModel):
    title = models.CharField(max_length=255, verbose_name="หัวข้อ")
    description = models.TextField(verbose_name="รายละเอียด")
    announce_date = models.DateTimeField(verbose_name="วันที่ประกาศ")
    expire_date = models.DateTimeField(blank=True, null=True, verbose_name="วันที่หมดอายุ")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="announcements",
        verbose_name="ผู้ประกาศ",
    )
    publish_status = models.CharField(
        max_length=20,
        choices=PublishStatusChoices.choices,
        default=PublishStatusChoices.DRAFT,
        verbose_name="สถานะเผยแพร่",
    )

    class Meta:
        verbose_name = "ประกาศ"
        verbose_name_plural = "ประกาศ"
        ordering = ["-announce_date"]

    def __str__(self) -> str:
        return self.title
