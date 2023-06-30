# from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
# from django.contrib.auth.decorators import login_required
# from django.http import HttpResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.contrib.auth.models import User
# from .models import Profile, Skill, userSkill
# from .forms import ProfileUpdateForm, SkillUpdateForm
# # from django import form
# from django.contrib.auth import get_user_model
# from recruiter.models import Job, Selected, Applicants
# from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
# from candidate.models import savedJobs, appliedJobs

# # Create your views here.


# def home(request):
#     return render(request, "candidate/home.html")


# def home_Candidate(request):
#     context = {"home_page": 'active'}
#     return render(request, "candidate/candidate_Home.html", context)


# # It displays the user profile and also the skills possessed by the user.
# @login_required
# def my_profile(request):
#     you = request.user  # Not User
#     profile = Profile.objects.filter(user=you).first()
#     skills = userSkill.objects.filter(user_skills=you)
#     print(profile)
#     if request.method == 'POST':
#         form = SkillUpdateForm(request.POST)
#         if form.is_valid():
#             data = form.save(commit=False)
#             data.user = you  # Play here
#             data.save()
#             return redirect('my-profile')
#     else:
#         form = SkillUpdateForm()
#     context = {
#         "user": you,
#         "data": profile,
#         "skills": skills,
#         "form": form,
#         "profil_Page": "active",
#     }
#     return render(request, "candidate/profile.html", context)


# # This function allows candidates to edit their profiles.
# @login_required
# def edit_profile(request):
#     you = request.user
#     profile = Profile.objects.filter(user=you).first()
#     if request.method == 'POST':
#         form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
#         if form.is_valid():
#             data = form.save(commit=False)
#             data.user = you
#             data.save()
#             return redirect('my-profile')
#     else:
#         form = ProfileUpdateForm(instance=profile)
#     context = {
#         "form": form,
#         # "profile":profile ,  #Pass Profile and Skills to upadte!

#     }

#     return render(request, 'candidate/edit_profile.html', context)


# @login_required
# def profile_view_for_recruiter(request, pk):  # Think about AutoSlug and user-> Who are accessing
#     # user=request.user
#     profile = Profile.objects.filter(id=pk)
#     user = profile.user
#     profile_skills = userSkill.objects.get(user=user)
#     context = {
#         "profile": profile,
#         "profile_skills": profile_skills,

#     }
#     return render(request, "cabdidate/   .html", context)


# @login_required
# def job_search_list(request):
#     search_query = request.GET.get("query")
#     search_location = request.GET.get("location")
#     query_list = []
#     if (search_query == None):  # For Location ...And,Or
#         job = Job.objects.all()
#     else:
#         find_title = Job.objects.filter(title__icontains=search_query).order_by(
#             "-posted_At")  # Updated_At ,values
#         find_company = Job.objects.filter(
#             company__icontains=search_query).order_by("-posted_At")
#         find_type = Job.objects.filter(
#             type__icontains=search_query).order_by("-posted_At")
#         find_skills = Job.objects.filter(
#             skills_required__icontains=search_query).order_by("-posted_At")

#         for i in find_title:
#             query_list.append(i)
#         for i in find_company:
#             query_list.append(i)
#         for i in find_type:
#             query_list.append(i)
#         for i in find_skills:
#             query_list.append(i)

#     if (search_location == None):  # Make Model Changes --> City
#         locat = Job.objects.all()
#     else:
#         locat = Job.objects.filter(
#             country__icontains=search_location).order_by("-posted_At")

#     final_query_list = []
#     for i in query_list:
#         if i in locat:
#             final_query_list.append(i)

#     # paginator = Paginator(final_query_list, 1)
#     # page=request.GET.get("page")
#     # # try:
#     # page_number = paginator.page(page)
#     # page_obj = paginator.get_page(page_number)
#     # except PageNotAnInteger:
#     #     page_number = paginator.page(1)
#     # except EmptyPage:
#     #     page_number = paginator.page(paginator.num_pages)
#     paginator = Paginator(final_query_list, 5)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     context = {
#         'jobs': page_obj,
#         'query': search_query,
#     }
#     return render(request, 'candidate/job_search_list.html', context)


# @login_required
# def saved_jobs(request):
#     jobs = savedJobs.objects.filter(
#         user=request.user).order_by('-posted_at')
#     return render(request, 'candidate/saved_Job.html', {'jobs': jobs, 'candidate_navbar': 1})


# @login_required
# def applied_jobs(request):
#     jobs = appliedJobs.objects.filter(
#         user=request.user).order_by('-posted_at')
#     statuses = []
#     for job in jobs:
#         if Selected.objects.filter(job=job.job).filter(applicant=request.user).exists():
#             statuses.append(0)
#         elif Applicants.objects.filter(job=job.job).filter(applicant=request.user).exists():
#             statuses.append(1)
#         else:
#             statuses.append(2)
#     zipped = zip(jobs, statuses)
#     return render(request, 'candidate/applied_Jobs.html', {'zipped': zipped, 'candidate_navbar': 1})


# @login_required
# def save_The_Given_Job(request, slug):
#     user = request.user
#     job = get_object_or_404(Job, slug=slug)
#     saved_Job, created = savedJobs.objects.get_or_create(job=job, user=user)
#     return HttpResponseRedirect('/job/{}'.format(job.slug))


# @login_required
# def apply_The_Given_Job(request, slug):
#     user = request.user
#     job = get_object_or_404(Job, slug=slug)
#     applied_Job, created = appliedJobs.objects.get_or_create(
#         job=job, user=user)
#     applicants, creation = Applicants.objects.get_or_create(
#         job=job, applicant=user)
#     return HttpResponseRedirect('/job/{}'.format(job.slug))


# @login_required
# def remove_The_Given_Job(request, slug):
#     user = request.user
#     job = get_object_or_404(Job, slug=slug)
#     saved_job = savedJobs.objects.filter(job=job, user=user).first()
#     saved_job.delete()
#     return HttpResponseRedirect('/job/{}'.format(job.slug))


# @login_required
# def job_Details(request, slug):
#     user = request.user
#     profile = Profile.objects.filter(user=user).first()
#     print(slug)
#     job = get_object_or_404(Job, slug=slug)
#     applied_button, saved_button = 0, 0
#     if (appliedJobs.objects.filter(user=user).filter(job=job).exists()):
#         applied_button = 1
#     if (savedJobs.objects.filter(user=user).filter(job=job).exists()):
#         saved_button = 1
#     context = {
#         'job': job,
#         'profile': profile,
#         'applied_button': applied_button,
#         'saved_button': saved_button,
#         # 'relevant_jobs': relevant_jobs,
#         'candidate_navbar': 1,
#     }
#     return render(request, 'candidate/job_details.html', context)

from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from .models import Profile, Skill, userSkill, Experience
from .forms import ProfileUpdateForm, SkillUpdateForm, ExperienceForm
from recruiter.models import Job, Selected, Applicants
from candidate.models import savedJobs, appliedJobs


class HomeView(View):
    def get(self, request):
        return render(request, "candidate/home.html")


class HomeCandidateView(View):
    def get(self, request):
        context = {"home_page": 'active'}
        return render(request, "candidate/candidate_Home.html", context)


class MyProfileView(LoginRequiredMixin, View):
    def get(self, request):
        you = request.user
        profile = Profile.objects.filter(user=you).first()
        skills = userSkill.objects.filter(user_skills=you)
        experience = Experience.objects.filter(user=you)
        skill_form = SkillUpdateForm()
        experience_form = ExperienceForm()
        context = {
            "user": you,
            "data": profile,
            "skills": skills,
            "skill_form": skill_form,
            "experience": experience,
            "experience_form": experience_form,
            "profile_Page": "active",
        }
        return render(request, "candidate/profile.html", context)

    def post(self, request):
        you = request.user
        skill_form = SkillUpdateForm(request.POST)
        experience_form = ExperienceForm(request.POST)
        if skill_form.is_valid():
            data = skill_form.save(commit=False)
            data.user_skills = you
            data.save()
            return redirect('my-profile')
        if experience_form.is_valid():
            data = experience_form.save(commit=False)
            data.user = you
            data.save()
            return redirect('my-profile')
        else:
            profile = Profile.objects.filter(user=you).first()
            skills = userSkill.objects.filter(user_skills=you)
            experience = Experience.objects.filter(user=you)

            context = {
                "user": you,
                "data": profile,
                "skills": skills,
                "skill_form": skill_form,
                "experience": experience,
                "experience_form": experience_form,
                "profile_Page": "active",
            }
            return render(request, "candidate/profile.html", context)


class EditProfileView(LoginRequiredMixin, View):
    def get(self, request):
        you = request.user
        profile = Profile.objects.filter(user=you).first()
        form = ProfileUpdateForm(instance=profile)
        context = {
            "form": form,
        }
        return render(request, 'candidate/edit_profile.html', context)

    def post(self, request):
        you = request.user
        profile = Profile.objects.filter(user=you).first()
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = you
            data.save()
            return redirect('my-profile')
        else:
            context = {
                "form": form,  # Pass Profile and Skills to upadte!
            }
            return render(request, 'candidate/edit_profile.html', context)


class ProfileViewForRecruiterView(LoginRequiredMixin, View):
    def get(self, request, slug):
        profile = Profile.objects.filter(user=slug)  
        print(profile)
        user = profile.user
        profile_skills = userSkill.objects.get(user=user)
        context = {
            "profile": profile,
            "profile_skills": profile_skills,
        }
        return render(request, "cabdidate/   .html", context)


class JobSearchListView(LoginRequiredMixin, View):
    def get(self, request):
        search_query = request.GET.get("query")
        search_location = request.GET.get("location")
        query_list = []
        if search_query is None:
            job = Job.objects.all()
        else:
            find_title = Job.objects.filter(
                title__icontains=search_query).order_by("-posted_At")
            find_company = Job.objects.filter(
                company__icontains=search_query).order_by("-posted_At")
            find_type = Job.objects.filter(
                type__icontains=search_query).order_by("-posted_At")
            find_skills = Job.objects.filter(
                skills_required__icontains=search_query).order_by("-posted_At")

            for i in find_title:
                query_list.append(i)
            for i in find_company:
                query_list.append(i)
            for i in find_type:
                query_list.append(i)
            for i in find_skills:
                query_list.append(i)

        if search_location is None:
            locat = Job.objects.all()
        else:
            locat = Job.objects.filter(
                country__icontains=search_location).order_by("-posted_At")

        final_query_list = []
        for i in query_list:
            if i in locat:
                final_query_list.append(i)

        paginator = Paginator(final_query_list, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'jobs': page_obj,
            'query': search_query,
        }
        return render(request, 'candidate/job_search_list.html', context)
# class JobSearchListView(LoginRequiredMixin, View):
#     def get(self, request):
#         search_query = request.GET.get("query")
#         search_location = request.GET.get("location")

#         query = Q(title__icontains=search_query) | Q(company__icontains=search_query) | Q(type__icontains=search_query) | Q(skills_required__icontains=search_query)
#         find_results = Job.objects.filter(query).order_by("-posted_At")

#         if search_location:
#             find_results = find_results.filter(country__icontains=search_location)

#         paginator = Paginator(find_results, 5)
#         page_number = request.GET.get('page')
#         page_obj = paginator.get_page(page_number)

#         context = {
#             'jobs': page_obj,
#             'query': search_query,
#         }

#         return render(request, 'candidate/job_search_list.html', context)


class SavedJobsView(LoginRequiredMixin, View):
    def get(self, request):
        jobs = savedJobs.objects.filter(
            user=request.user).order_by('-posted_at')
        return render(request, 'candidate/saved_Job.html', {'jobs': jobs, 'candidate_navbar': 1})


class AppliedJobsView(LoginRequiredMixin, View):
    def get(self, request):
        jobs = appliedJobs.objects.filter(
            user=request.user).order_by('-posted_at')
        statuses = []
        for job in jobs:
            if Selected.objects.filter(job=job.job).filter(applicant=request.user).exists():
                statuses.append(0)
            elif Applicants.objects.filter(job=job.job).filter(applicant=request.user).exists():
                statuses.append(1)
            else:
                statuses.append(2)
        zipped = zip(jobs, statuses)
        return render(request, 'candidate/applied_Jobs.html', {'zipped': zipped, 'candidate_navbar': 1})


class SaveJobView(LoginRequiredMixin, View):
    def get(self, request, slug):
        user = request.user
        job = get_object_or_404(Job, slug=slug)
        saved_Job, created = savedJobs.objects.get_or_create(
            job=job, user=user)
        return HttpResponseRedirect('/job/{}'.format(job.slug))


class ApplyJobView(LoginRequiredMixin, View):
    def get(self, request, slug):
        user = request.user
        job = get_object_or_404(Job, slug=slug)
        applied_Job, created = appliedJobs.objects.get_or_create(
            job=job, user=user)
        applicants, creation = Applicants.objects.get_or_create(
            job=job, applicant=user)
        return HttpResponseRedirect('/job/{}'.format(job.slug))


class RemoveJobView(LoginRequiredMixin, View):
    def get(self, request, slug):
        user = request.user
        job = get_object_or_404(Job, slug=slug)
        saved_job = savedJobs.objects.filter(job=job, user=user).first()
        saved_job.delete()
        return HttpResponseRedirect('/job/{}'.format(job.slug))


class JobDetailsView(LoginRequiredMixin, View):
    def get(self, request, slug):
        user = request.user
        profile = Profile.objects.filter(user=user).first()
        job = get_object_or_404(Job, slug=slug)
        applied_button, saved_button = 0, 0
        if appliedJobs.objects.filter(user=user).filter(job=job).exists():
            applied_button = 1
        if savedJobs.objects.filter(user=user).filter(job=job).exists():
            saved_button = 1
        relevant_jobs = []
        jobs1 = Job.objects.filter(
            company__icontains=job.company).order_by('-date_posted')
        jobs2 = Job.objects.filter(
            job_type__icontains=job.job_type).order_by('-date_posted')
        jobs3 = Job.objects.filter(
            title__icontains=job.title).order_by('-date_posted')
        for i in jobs1:
            if len(relevant_jobs) > 5:
                break
            if i not in relevant_jobs and i != job:
                relevant_jobs.append(i)
        for i in jobs2:
            if len(relevant_jobs) > 5:
                break
            if i not in relevant_jobs and i != job:
                relevant_jobs.append(i)
        for i in jobs3:
            if len(relevant_jobs) > 5:
                break
        if i not in relevant_jobs and i != job:
            relevant_jobs.append(i)

        context = {
            'job': job,
            'profile': profile,
            'applied_button': applied_button,
            'saved_button': saved_button,
            'candidate_navbar': 1,
        }
        return render(request, 'candidate/job_details.html', context)


class DeleteSkillView(LoginRequiredMixin, View):
    def post(self, request, pk=None):
        id_list = request.POST.getlist('choices')
        id_list1 = []
        for skill_id in id_list:
            id1 = Skill.objects.get(skills=skill_id).id
            id_list1.append(id1)
        for ids in id_list1:
            userSkill.objects.get(skills=ids).delete()

        return redirect('my-profile')
