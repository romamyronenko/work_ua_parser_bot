def prettify_job(job: dict):
    """{'title': 'Python Developer in Test',
    'company': 'Ajax Systems',
    'url': 'https://www.work.ua/jobs/5681643/',
    'address': 'Київ, вулиця Семена Скляренка, 5. 6,2 км від центру'}"""
    return f"""{job.get('title')}\n{job.get('company')}\n{job.get('address')}\n{job.get('url')}"""
