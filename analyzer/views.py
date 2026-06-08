from .gemini_helper import get_resume_feedback
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm
from django.shortcuts import redirect
from django.shortcuts import render
import pdfplumber

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import ResumeAnalysis
skills_list = [
    "python",
    "django",
    "react",
    "javascript",
    "html",
    "css",
    "sql",
    "machine learning",
    "tensorflow",
    "keras",
    "api",
    "git",
    "docker",
    "mongodb",
    "postgresql"
]

@login_required(login_url='/login/')
def home(request):

    extracted_text = ""
    match_score = 0

    if request.method == 'POST':
        missing_skills = []
        suggestions = []
        ai_feedback = ""

        uploaded_resume = request.FILES.get('resume')

        job_description = request.POST.get('job_description')

        if uploaded_resume:

            with pdfplumber.open(uploaded_resume) as pdf:

                for page in pdf.pages:

                    text = page.extract_text()

                    if text:
                        extracted_text += text

        documents = [extracted_text, job_description]

        tfidf = TfidfVectorizer()

        tfidf_matrix = tfidf.fit_transform(documents)

        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])

        match_score = round(similarity[0][0] * 100, 2)
        ResumeAnalysis.objects.create(
            user=request.user,
            job_description=job_description,
            resume_text=extracted_text,
            match_score=match_score,
        )
        resume_lower = extracted_text.lower()

        job_description_lower = job_description.lower()

        for skill in skills_list:

            if skill in job_description_lower and skill not in resume_lower:

                missing_skills.append(skill)
                suggestions.append(f"Consider adding {skill} related experience or projects.")
                try:
                    ai_feedback = get_resume_feedback(
                        extracted_text,
                        job_description
                    )
                except Exception:
                    ai_feedback = "AI feedback is temporarily unavailable. Please try again later."

        return render(request, 'analyzer/home.html', {
            'message': 'Resume uploaded successfully!',
            'resume_text': extracted_text,
            'missing_skills': missing_skills,
            'suggestions': suggestions,
            'match_score': match_score,
            'ai_feedback': ai_feedback
        })

    return render(request, 'analyzer/home.html')

@login_required(login_url='/login/')
def history(request):

    analyses = ResumeAnalysis.objects.filter(
    user=request.user
).order_by('-created_at')

    return render(request, 'analyzer/history.html', {
        'analyses': analyses
    })

def register(request):

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect('/')

    else:

        form = RegisterForm()

    return render(request, 'analyzer/register.html', {
        'form': form
    })

def user_login(request):

    if request.method == 'POST':

        username = request.POST.get('username')

        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('/')

    return render(request, 'analyzer/login.html')

def user_logout(request):

    logout(request)

    return redirect('/login/')