import requests
from bs4 import BeautifulSoup


def get_jobs(name: str, city: str) -> list[dict]:
    """
    title
    company
    short description
    salary(if available)
    url
    """
    url = f"https://www.work.ua/jobs-{city}-"
    # query = input("Введіть назву вакансії: ")
    name = name.replace(" ", "+")
    url += name
    response = requests.get(url)

    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    retval = []

    for div in soup.find_all(
            "div",
            class_="card card-hover card-search card-visited wordwrap job-link js-job-link-blank mt-lg",
    ) + soup.find_all(
        "div",
        class_="card card-hover card-search card-visited wordwrap job-link js-job-link-blank",
    ):
        job = {
            "title": get_title(div),
            "company": get_company(div)
        }
        salary = get_salary(div)
        if salary:
            job['salary'] = salary

        details = get_details(div)

        retval.append({**job, **details})

    return retval


def get_salary(div):
    salary_div = div.find("div", class_=None)
    if salary_div:
        return salary_div.span.text


def get_company(div):
    company_div = div.find("div", class_="mt-xs")

    return company_div.span.text


def get_title(div):
    return div.h2.a.text


def get_details(div):
    id_ = div.find("h2", class_="my-0").a["href"]
    url = f"https://www.work.ua{id_}"
    response = requests.get(url)

    html = response.text
    soup_ = BeautifulSoup(html, "html.parser")

    info_ul = soup_.find("ul", class_="list-unstyled sm:mt-2xl mt-lg mb-0")

    address_li = info_ul.find_all("li", class_="text-indent no-style mt-sm mb-0")

    retval = {'url': url}

    for li in address_li:
        if li.span["title"] == "Адреса роботи":
            address = li.text.split()
            address = " ".join(address)
            address = address.replace("На мапі", "")
            retval['address'] = address

            # print(address)

    phone_span = soup_.find("span", id="contact-phone")
    if phone_span:
        retval['phone'] = phone_span.a.text
    return retval
