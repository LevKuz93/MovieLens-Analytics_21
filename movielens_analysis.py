from collections import Counter, OrderedDict, defaultdict
import os
from bs4 import BeautifulSoup
import pytest
import re
from datetime import datetime

import requests


class Tags:
    """
    Analyzing data from tags.csv
    """

    def __init__(self, path_to_the_file):
        """
        Put here any fields that you think you will need.
        """
        self.path = path_to_the_file
        self.list_1000_strings = self.parse_1000_strings()

    def most_words(self, n):
        """
               The method returns top-n tags with most words inside. It is a dict
        where the keys are tags and the values are the number of words inside the tag.
        Drop the duplicates. Sort it by numbers descendingly.
        """
        if not isinstance(n, int) or n <= 0:
            raise ValueError(f"Неверное значение аргумента: {n}")
        unique_tags = self.take_unique_tags()
        big_tags = sorted(unique_tags, key=lambda x: len(x.split()), reverse=True)[:n]
        top_n = {tag: len(tag.split()) for tag in big_tags}
        return top_n

    def longest(self, n):
        """
        The method returns top-n longest tags in terms of the number of characters.
        It is a list of the tags. Drop the duplicates. Sort it by numbers descendingly.
        """
        if not isinstance(n, int) or n <= 0:
            raise ValueError(f"Неверное значение аргумента: {n}")
        unique_tags = self.take_unique_tags()
        big_tags = sorted(unique_tags, key=lambda x: len(x), reverse=True)[:n]
        return big_tags

    def most_words_and_longest(self, n):
        """
        The method returns the intersection between top-n tags with most words inside and
        top-n longest tags in terms of the number of characters.
        Drop the duplicates. It is a list of the tags.
        """
        if not isinstance(n, int) or n <= 0:
            raise ValueError(f"Неверное значение аргумента: {n}")
        mwd = self.most_words(n)
        lgst = self.longest(n)
        intersection = list(set(mwd.keys()) & set(lgst))

        return intersection

    def most_popular(self, n):
        """
        The method returns the most popular tags.
        It is a dict where the keys are tags and the values are the counts.
        Drop the duplicates. Sort it by counts descendingly.
        """
        if not isinstance(n, int) or n <= 0:
            raise ValueError(f"Неверное значение аргумента: {n}")
        tags = [
            self.list_1000_strings[i][2] for i in range(1, len(self.list_1000_strings))
        ]
        tag_counts = Counter(tags)
        popular_tags = tag_counts.most_common(n)
        return dict(popular_tags)

    def tags_with(self, word):
        """
        The method returns all unique tags that include the word given as the argument.
        Drop the duplicates. It is a list of the tags. Sort it by tag names alphabetically.
        """
        if not isinstance(word, str):
            raise ValueError(f"Неверное значение аргумента: {word}")
        unique_tags = self.take_unique_tags()
        tags_with_word = [tag for tag in unique_tags if word.lower() in tag.lower()]
        return sorted(tags_with_word)

    def parse_1000_strings(self):
        """
        The method returns list of 1000 first strings
        """
        if not os.path.isfile(self.path) or os.path.getsize(self.path) == 0:
            raise FileNotFoundError(f"Файл не найден или пустой: {self.path}")
        row = []
        with open(self.path, "r", encoding="utf-8") as file:
            for _ in range(1001):
                line = file.readline().strip()
                if line:
                    row.append(line.split(","))
            return row

    def take_unique_tags(self):
        """
        The method returns set of unique tags
        """
        unique_tags = list(
            set(
                self.list_1000_strings[i][2]
                for i in range(1, len(self.list_1000_strings))
            )
        )
        return unique_tags


class Movies:
    """
    Analyzing data from movies.csv
    """

    def __init__(self, path_to_the_file):
        """
        Put here any fields that you think you will need.
        """
        self.path = path_to_the_file
        self.lst = self.parse_1000_strings()
        # self.dist_by_release()
        # self.most_genres(5)

    def dist_by_release(self):
        """
        The method returns a dict or an OrderedDict where the keys are years and the values are counts.
        You need to extract years from the titles. Sort it by counts descendingly.
        """
        # years_extracted = [int(re.search(r'\((.*?)\)', el)) for el in self.lst]
        years_extracted = []
        for i in range(1, len(self.lst)):
            el = self.lst[i]
            title = el[1]
            match = re.search(r"\((\d{4})\)", title)
            if match:
                years_extracted.append(int(match.group(1)))

        release_years = Counter(years_extracted)
        sorted_years = OrderedDict(release_years.most_common())
        # print(sorted_years)
        return sorted_years

    def dist_by_genres(self):
        """
           The method returns a dict where the keys are genres and the values are counts.
        Sort it by counts descendingly.
        """
        genres = []
        for i in range(1, len(self.lst)):
            el = self.lst[i]
            title = el[2]
            genres.extend(t.strip() for t in title.split("|") if t.strip())

        dict_of_genres = Counter(genres)
        genres = dict(dict_of_genres.most_common())
        # print(genres)
        return genres

    def most_genres(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are the number of genres of the movie. Sort it by numbers descendingly.
        """
        if not isinstance(n, int) or n <= 0:
            raise ValueError(f"Неверное значение аргумента: {n}")
        movies = []
        for i in range(1, len(self.lst)):
            el = self.lst[i]
            title = el[2]
            count = 0
            for t in title.split("|"):
                if t.strip():
                    count += 1

            movies.append([el[1], count])

        sorted_movies = sorted(movies, key=lambda x: x[1], reverse=True)
        movies = dict(sorted_movies[:n])
        # print(movies)
        return movies

    def parse_1000_strings(self):
        """
        The method returns list of 1000 first strings
        """
        if not os.path.isfile(self.path) or os.path.getsize(self.path) == 0:
            raise FileNotFoundError(f"Файл не найден или пустой: {self.path}")

        pattern = re.compile(r',(?=(?:(?:[^"]*"){2})*[^"]*$)')
        row = []
        with open(self.path, "r", encoding="utf-8") as file:
            for _ in range(1001):
                line = file.readline().strip()
                if line:
                    row.append(pattern.split(line))
            return row


class Links:
    def __init__(self, path_to_links, path_to_movies):
        self.movie_data = {}
        self.session = requests.Session()

        if not os.path.isfile(path_to_movies) or os.path.getsize(path_to_movies) == 0:
            raise FileNotFoundError(f"Файл не найден или пустой: {path_to_movies}")
        with open(path_to_movies, "r", encoding="utf-8") as f:
            next(f)
            for i, line in enumerate(f):
                if i >= 1000:
                    break
                parts = re.split(r',(?=(?:[^"]*"[^"]*")*[^"]*$)', line.strip())
                if len(parts) >= 2:
                    try:
                        m_id = int(parts[0])
                        self.movie_data[m_id] = {"title": parts[1].strip('"')}
                    except (ValueError, IndexError):
                        continue

        if not os.path.isfile(path_to_links) or os.path.getsize(path_to_links) == 0:
            raise FileNotFoundError(f"Файл не найден или пустой: {path_to_links}")
        with open(path_to_links, "r", encoding="utf-8") as f:
            next(f)
            for i, line in enumerate(f):
                if i >= 1000:
                    break
                parts = line.strip().split(",")
                try:
                    m_id = int(parts[0])
                    if m_id in self.movie_data and len(parts) > 2 and parts[2]:
                        self.movie_data[m_id]["tmdbId"] = parts[2]
                except (ValueError, IndexError):
                    continue

    def get_tmdb(self, list_of_movies, list_of_fields):
        tmdb_info = []

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
        }

        for m_id in list_of_movies:
            if m_id not in self.movie_data or "tmdbId" not in self.movie_data[m_id]:
                continue

            tmdb_id = self.movie_data[m_id]["tmdbId"]
            url = f"https://www.themoviedb.org/movie/{tmdb_id}"

            try:
                response = self.session.get(url, headers=headers, timeout=10)
                if response.status_code != 200:
                    continue

                soup = BeautifulSoup(response.text, "html.parser")

                parsed_data = {
                    "Director": "N/A",
                    "Budget": 0,
                    "Revenue": 0,
                    "Runtime": 0,
                    "Status": "N/A",
                    "Released": "N/A",
                    "Original Language": "N/A",
                    "Novel": [],
                    "Screenplay": [],
                }

                facts_section = soup.find("section", class_="facts")
                profiles = soup.find_all("li", class_="profile")
                runtime_span = soup.find("span", class_="runtime")

                if facts_section:
                    facts_text_pipe = facts_section.get_text(separator="|").strip()
                    facts_text_space = facts_section.get_text(separator=" ").strip()

                    status_match = re.search(r"Status\s*\|\s*([^|]+)", facts_text_pipe)
                    if status_match:
                        parsed_data["Status"] = status_match.group(1).strip()

                    released_match = re.search(
                        r"Released\s*\|\s*([A-Za-z]+\s+\d{1,2},?\s+\d{4})",
                        facts_text_pipe,
                    )
                    if released_match:
                        parsed_data["Released"] = released_match.group(1).strip()

                    orig_lang_match = re.search(
                        r"Original Language\s*\|\s*([A-Za-z]+)", facts_text_pipe
                    )
                    if orig_lang_match:
                        parsed_data["Original Language"] = orig_lang_match.group(
                            1
                        ).strip()

                    budget_match = re.search(
                        r"Budget\s+\$([\d,]+(?:\.\d+)?)", facts_text_space
                    )
                    if budget_match:
                        parsed_data["Budget"] = int(
                            budget_match.group(1).replace(",", "").split(".")[0]
                        )

                    revenue_match = re.search(
                        r"Revenue\s+\$([\d,]+(?:\.\d+)?)", facts_text_space
                    )
                    if revenue_match:
                        parsed_data["Revenue"] = int(
                            revenue_match.group(1).replace(",", "").split(".")[0]
                        )

                if runtime_span:
                    runtime_text = runtime_span.text.strip()
                    hours = re.search(r"(\d+)h", runtime_text)
                    minutes = re.search(r"(\d+)m", runtime_text)
                    total_minutes = 0
                    if hours:
                        total_minutes += int(hours.group(1)) * 60
                    if minutes:
                        total_minutes += int(minutes.group(1))
                    if total_minutes > 0:
                        parsed_data["Runtime"] = total_minutes

                # 🔹 Парсим профили (Director, Novel, Screenplay)
                for profile in profiles:
                    character_p = profile.find("p", class_="character")
                    if not character_p:
                        continue
                    role = character_p.text.strip()
                    name_a = profile.find("a")
                    if not name_a:
                        continue

                    if "Director" in role:
                        parsed_data["Director"] = name_a.text.strip()
                    elif role == "Novel":
                        parsed_data["Novel"].append(name_a.text.strip())
                    elif role == "Screenplay":
                        parsed_data["Screenplay"].append(name_a.text.strip())

                row = [m_id]
                for field in list_of_fields:
                    if field in ["Cumulative Worldwide Gross", "Revenue"]:
                        row.append(parsed_data["Revenue"])
                    elif field in parsed_data:
                        value = parsed_data[field]
                        if isinstance(value, list):
                            value = ", ".join(value) if value else "N/A"
                        row.append(value)
                    else:
                        row.append("N/A")

                for idx, field in enumerate(list_of_fields):
                    self.movie_data[m_id][field] = row[idx + 1]

                tmdb_info.append(row)

            except Exception as e:
                continue

        tmdb_info.sort(key=lambda x: x[0], reverse=True)
        return tmdb_info

    def top_directors(self, n):
        if not isinstance(n, int) or n <= 0:
            raise ValueError(f"Неверное значение аргумента: {n}")
        dirs = [
            m.get("Director")
            for m in self.movie_data.values()
            if m.get("Director") and m["Director"] != "N/A"
        ]
        return dict(sorted(Counter(dirs).items(), key=lambda x: x[1], reverse=True)[:n])

    def most_expensive(self, n):
        if not isinstance(n, int) or n <= 0:
            raise ValueError(f"Неверное значение аргумента: {n}")
        data = [
            (m["title"], m.get("Budget", 0))
            for m in self.movie_data.values()
            if "Budget" in m
        ]
        return dict(sorted(data, key=lambda x: x[1], reverse=True)[:n])

    def most_profitable(self, n):
        if not isinstance(n, int) or n <= 0:
            raise ValueError(f"Неверное значение аргумента: {n}")
        data = [
            (m["title"], m["Revenue"] - m["Budget"])
            for m in self.movie_data.values()
            if "Revenue" in m and "Budget" in m
        ]
        return dict(sorted(data, key=lambda x: x[1], reverse=True)[:n])

    def longest(self, n):
        if not isinstance(n, int) or n <= 0:
            raise ValueError(f"Неверное значение аргумента: {n}")
        data = [
            (m["title"], m.get("Runtime", 0))
            for m in self.movie_data.values()
            if "Runtime" in m
        ]
        return dict(sorted(data, key=lambda x: x[1], reverse=True)[:n])

    def top_cost_per_minute(self, n):
        if not isinstance(n, int) or n <= 0:
            raise ValueError(f"Неверное значение аргумента: {n}")
        data = []
        for m in self.movie_data.values():
            if m.get("Runtime", 0) > 0 and "Budget" in m:
                data.append((m["title"], round(m["Budget"] / m["Runtime"], 2)))
        return dict(sorted(data, key=lambda x: x[1], reverse=True)[:n])


class Ratings:
    """
    Analyzing data from ratings.csv
    """

    def __init__(
        self,
        path_to_ratings="./datasets/ratings.csv",
        path_to_movies="./datasets/movies.csv",
        limit=1000,
    ):
        """
        Put here any fields that you think you will need.
        """
        if not os.path.isfile(path_to_ratings) or os.path.getsize(path_to_ratings) == 0:
            raise FileNotFoundError(f"Файл не найден или пустой: {path_to_ratings}")
        if not os.path.isfile(path_to_movies) or os.path.getsize(path_to_movies) == 0:
            raise FileNotFoundError(f"Файл не найден или пустой: {path_to_movies}")

        self.path_to_the_file = path_to_ratings
        self.limit = int(limit)
        self.data = []
        self.path_to_movies = path_to_movies
        self.movie_data = Movies(path_to_movies).parse_1000_strings()

    def read_csv_to_dicts(self):
        """
        The method returns list of dictionaries in self.data
        """
        with open(self.path_to_the_file, "r", encoding="utf-8") as file:
            header = file.readline().strip().split(",")
            header = [h.strip() for h in header]
            for i, line in enumerate(file):
                if i < self.limit:
                    values = line.strip().split(",")
                    values = [v.strip() for v in values]
                    row_dict = dict(zip(header, values))
                    self.data.append(row_dict)
        return self.data

    class Movies:
        def __init__(self, outer):
            if not isinstance(outer, Ratings):
                raise TypeError("Аргумент должен быть экземпляром класса Ratings")
            self.data = outer.data
            self.movie_data = outer.movie_data

        def dist_by_year(self):
            """
            The method returns a dict where the keys are years and the values are counts.
            Sort it by years ascendingly. You need to extract years from timestamps.
            """
            ratings_by_year = []
            for row in self.data:
                year = datetime.fromtimestamp(int(row["timestamp"])).year
                ratings_by_year.append(year)
            return dict(
                sorted(Counter(ratings_by_year).items())
            )  # Sort it by years ascendingly

        def dist_by_rating(self):
            """
               The method returns a dict where the keys are ratings and the values are counts.
            Sort it by ratings ascendingly.
            """
            ratings_distribution = []
            for row in self.data:
                rating = row["rating"]
                ratings_distribution.append(rating)
            return dict(
                sorted(Counter(ratings_distribution).items(), key=lambda x: float(x[0]))
            )

        def data_movie_id_title(self):
            """
               The method returns a dict where the keys are ratings and the values are counts.
            Sort it by ratings ascendingly.
            """
            movie_id_title = {
                row[0]: row[1].rsplit(" (", 1)[0].replace('"', "")
                for row in self.movie_data[1:]
            }
            for row in self.data:
                row["title"] = movie_id_title.get(row["movieId"])
            return self.data

        def top_by_num_of_ratings(self, n):
            """
                   The method returns top-n movies by the number of ratings.
                   It is a dict where the keys are movie titles and the values are numbers.
            Sort it by numbers descendingly.
            """
            if not isinstance(n, int) or n <= 0:
                raise ValueError(f"Неверное значение аргумента: {n}")

            movie_title = []
            for row in self.data_movie_id_title():
                if row["title"]:
                    movie_title.append(row["title"])
            return dict(
                sorted(Counter(movie_title).items(), key=lambda x: x[1], reverse=True)[
                    :n
                ]
            )

        def average(self, values):
            """
            The method returns a mean of values
            """
            return round(sum(values) / len(values), 2) if values else 0

        def median(self, values):
            """
            The method returns a median of values
            """
            result = 0
            if values:
                sorted_vals = sorted(values)
                n = len(sorted_vals)
                mid = n // 2
                if n % 2 == 1:
                    result = sorted_vals[mid]
                else:
                    result = (sorted_vals[mid - 1] + sorted_vals[mid]) / 2
            return result

        def top_by_ratings(self, n=5, metric="average"):
            """
            The method returns top-n movies by the average or median of the ratings.
            It is a dict where the keys are movie titles and the values are metric values.
            Sort it by metric descendingly.
            The values should be rounded to 2 decimals.
            """
            if not isinstance(n, int) or n <= 0 or metric not in ["average", "median"]:
                raise ValueError(f"Неверное значение аргумента: {n,metric}")

            if metric == "average":
                metric = self.average
            else:
                metric = self.median

            ratings = defaultdict(list)
            for row in self.data_movie_id_title():
                movie_title = str(row["title"])
                rating = float(row["rating"])
                ratings[movie_title].append(rating)

            metric_values = {}
            for movie_title, rating_list in ratings.items():
                if rating_list and movie_title:
                    value = round(metric(rating_list), 2)
                    metric_values[movie_title] = value

            top_movies = dict(
                sorted(metric_values.items(), key=lambda x: x[1], reverse=True)[:n]
            )
            return top_movies

        def variance(self, lst):
            """
            The method returns a variance of values
            """
            result = 0
            if lst:
                mean = sum(lst) / len(lst)
                result = sum((x - mean) ** 2 for x in lst) / len(lst)
            return result

        def top_controversial(self, n=5):
            """
              The method returns top-n movies by the variance of the ratings.
              It is a dict where the keys are movie titles and the values are the variances.
            Sort it by variance descendingly.
              The values should be rounded to 2 decimals.
            """
            if not isinstance(n, int) or n <= 0:
                raise ValueError(f"Неверное значение аргумента: {n}")

            ratings = defaultdict(list)
            for row in self.data_movie_id_title():
                movie_title = str(row["title"])
                rating = float(row["rating"])
                ratings[movie_title].append(rating)

            variance_dict = {}
            for movie_title, rating_list in ratings.items():
                if (
                    movie_title and len(rating_list) >= 2
                ):  # дисперсия работает от 2х значений
                    var = round(self.variance(rating_list), 2)
                    variance_dict[movie_title] = var
            top_movies = dict(
                sorted(variance_dict.items(), key=lambda x: x[1], reverse=True)[:n]
            )
            return top_movies

    class Users(Movies):
        """
           In this class, three methods should work.
           The 1st returns the distribution of users by the number of ratings made by them.
           The 2nd returns the distribution of users by average or median ratings made by them.
           The 3rd returns top-n users with the biggest variance of their ratings.
        Inherit from the class Movies. Several methods are similar to the methods from it.
        """

        def __init__(self, outer):
            self.data = outer.data

        def dist_by_num_of_rating(self):
            """
            The 1st method returns the distribution of users by the number of ratings made by them.
            """
            user_ratings_count = Counter()
            for row in self.data:
                user_id = row["userId"]
                user_ratings_count[user_id] += 1
            user_ratings_count = dict(
                sorted(user_ratings_count.items(), key=lambda x: x[1], reverse=True)
            )
            return user_ratings_count

        def dist_by_rating_values(self, metric="average"):
            """
            The 2nd returns the distribution of users by average or median ratings made by them. From the most loyal to the most critical
            """
            if metric not in ["average", "median"]:
                raise ValueError(f"Неверное значение аргумента: {metric}")
            ratings = defaultdict(list)
            for row in self.data:
                user_id = row["userId"]
                rating = float(row["rating"])
                ratings[user_id].append(rating)
            func = self.average if metric == "average" else self.median
            user_metrics = {
                user_id: round(func(rating_list), 2)
                for user_id, rating_list in ratings.items()
            }
            return dict(sorted(user_metrics.items(), key=lambda x: x[1], reverse=True))

        def top_controversial_users(self, n):
            """
            The 3rd returns top-n users with the biggest variance of their ratings.
            """
            if not isinstance(n, int) or n <= 0:
                raise ValueError(f"Неверное значение аргумента: {n}")

            ratings = defaultdict(list)
            for row in self.data:
                user_id = row["userId"]
                rating = float(row["rating"])
                ratings[user_id].append(rating)
            user_variances = {}
            for user_id, rating_list in ratings.items():
                if len(rating_list) >= 2:
                    var = round(self.variance(rating_list), 2)
                    user_variances[user_id] = var
            return dict(
                sorted(user_variances.items(), key=lambda x: x[1], reverse=True)[:n]
            )


class Test:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.folder = "./ml-latest-small"
        self.tags = Tags(f"{self.folder}/tags.csv")
        self.movies = Movies(f"{self.folder}/movies.csv")
        self.links = Links(f"{self.folder}/links.csv", f"{self.folder}/movies.csv")
        self.ratings_fixture = Ratings(
            path_to_ratings=f"{self.folder}/ratings.csv",
            path_to_movies=f"{self.folder}/movies.csv",
            limit=100,
        )
        self.rating_movies = Ratings.Movies(self.ratings_fixture)
        self.users = Ratings.Users(self.ratings_fixture)

    # _________________________TAGS________________________________

    def test_most_words(self):
        n = 5
        result = self.tags.most_words(n)

        assert isinstance(result, dict)
        assert len(result) <= n

        for tag, count in result.items():
            assert isinstance(tag, str)
            assert isinstance(count, int)

        counts = list(result.values())
        assert counts == sorted(counts, reverse=True)

    def test_longest(self):
        n = 5
        result = self.tags.longest(n)

        assert isinstance(result, list)

        for tag in result:
            assert isinstance(tag, str)

        lengths = [len(t) for t in result]
        assert lengths == sorted(lengths, reverse=True)

    def test_most_popular(self):
        n = 5
        result = self.tags.most_popular(n)

        assert isinstance(result, dict)

        for tag, count in result.items():
            assert isinstance(tag, str)
            assert isinstance(count, int)

        counts = list(result.values())
        assert counts == sorted(counts, reverse=True)

    def test_tags_with(self):
        word = "sci"
        result = self.tags.tags_with(word)

        assert isinstance(result, list)

        for tag in result:
            assert isinstance(tag, str)
            assert word.lower() in tag.lower()

        assert result == sorted(result)

    def test_most_words_and_longest(self):
        n = 5
        result = self.tags.most_words_and_longest(n)

        assert isinstance(result, list)
        assert all(isinstance(t, str) for t in result)

        mwd = self.tags.most_words(n)
        lgst = self.tags.longest(n)
        for tag in result:
            assert tag in mwd
            assert tag in lgst

    def test_parse_1000_strings_tags(self):
        assert len(self.tags.list_1000_strings) == 1001

    def test_take_unique_tags(self):
        unique_tags = self.tags.take_unique_tags()
        assert isinstance(unique_tags, list)

    # ___________________________MOVIES___________________

    def test_dist_by_release(self):
        result = self.movies.dist_by_release()

        assert isinstance(result, OrderedDict)

        for year, count in result.items():
            assert isinstance(year, int)
            assert isinstance(count, int)

    def test_dist_by_genres(self):
        result = self.movies.dist_by_genres()

        assert isinstance(result, dict)

        for genre, count in result.items():
            assert isinstance(genre, str)
            assert isinstance(count, int)

    def test_most_genres(self):
        n = 5
        result = self.movies.most_genres(n)

        assert isinstance(result, dict)
        assert len(result) <= n

        for title, count in result.items():
            assert isinstance(title, str)
            assert isinstance(count, int)

    def parse_parse_1000_strs_for_movies(self):
        assert len(self.movies.list_1000_strings) == 1001

    # ___________________________LINKS___________________

    def test_top_directors(self):
        n = 5
        result = self.links.top_directors(n)

        assert isinstance(result, dict)
        assert len(result) <= n

        for director, count in result.items():
            assert isinstance(director, str)
            assert isinstance(count, int)

        counts = list(result.values())
        assert counts == sorted(counts, reverse=True)

    def test_most_expensive(self):
        n = 5
        result = self.links.most_expensive(n)

        assert isinstance(result, dict)
        assert len(result) <= n

        for title, budget in result.items():
            assert isinstance(title, str)
            assert isinstance(budget, int)

        budgets = list(result.values())
        assert budgets == sorted(budgets, reverse=True)

    def test_most_profitable(self):
        n = 5
        result = self.links.most_profitable(n)

        assert isinstance(result, dict)
        assert len(result) <= n

        for title, profit in result.items():
            assert isinstance(title, str)
            assert isinstance(profit, int)

        profits = list(result.values())
        assert profits == sorted(profits, reverse=True)

    def test_longest(self):
        n = 5
        result = self.links.longest(n)

        assert isinstance(result, dict)
        assert len(result) <= n

        for title, runtime in result.items():
            assert isinstance(title, str)
            assert isinstance(runtime, int)

        runtimes = list(result.values())
        assert runtimes == sorted(runtimes, reverse=True)

    def test_top_cost_per_minute(self):
        n = 5
        result = self.links.top_cost_per_minute(n)

        assert isinstance(result, dict)
        assert len(result) <= n

        for title, cost in result.items():
            assert isinstance(title, str)
            assert isinstance(cost, float)

        costs = list(result.values())
        assert costs == sorted(costs, reverse=True)

    # ___________________________RATINGS___________________

    def test_file_path(self):
        path_to_ratings = f"{self.folder}/ratings.csv"
        path_to_movies = f"{self.folder}/movies.csv"
        assert os.path.isfile(
            path_to_ratings
        ), f"Файл должен существовать: {path_to_ratings}"
        assert os.path.isfile(
            path_to_movies
        ), f"Файл должен существовать: {path_to_movies}"

    def test_load_ratings(self):
        r = self.ratings_fixture.read_csv_to_dicts()
        assert isinstance(r, list), "Data should be a list"

    def test_dist_by_year(self):
        result = self.rating_movies.dist_by_year()
        assert isinstance(result, dict), "Result should be a dictionary"
        assert all(
            isinstance(year, int) for year in result.keys()
        ), "Year should be an integer"
        assert all(
            isinstance(count, int) for count in result.values()
        ), "Count should be an integer"
        sorted_years = sorted(result.values())
        assert list(result.values()) == sorted_years, "Result should be sorted by year"

    def test_dist_by_rating(self):
        result = self.rating_movies.dist_by_rating()
        assert isinstance(result, dict), "Result should be a dictionary"
        assert all(
            isinstance(rating, float) for rating in result.keys()
        ), "Rating should be a float"
        assert all(
            isinstance(count, int) for count in result.values()
        ), "Count should be an integer"
        sorted_ratings = sorted(result.values())
        assert (
            list(result.values()) == sorted_ratings
        ), "Result should be sorted by rating"

    def test_top_by_num_of_ratings(self):
        result = self.rating_movies.top_by_num_of_ratings(10)
        assert isinstance(result, dict), "Result should be a dictionary"
        assert all(
            isinstance(title, str) for title in result.keys()
        ), "Movie title should be a string"
        assert all(
            isinstance(count, int) for count in result.values()
        ), "Count should be an integer"
        sorted_by_count = sorted(result.items(), key=lambda x: x[1], reverse=True)
        assert (
            list(result.items()) == sorted_by_count
        ), "Result should be sorted by count descending"

    def test_top_by_ratings(self):
        result = self.rating_movies.top_by_ratings(10)
        assert isinstance(result, dict), "Result should be a dictionary"
        assert all(
            isinstance(title, str) for title in result.keys()
        ), "Movie title should be a string"
        assert all(
            isinstance(avg_rating, float) for avg_rating in result.values()
        ), "Average rating should be a float"
        sorted_by_rating = sorted(result.items(), key=lambda x: x[1], reverse=True)
        assert (
            list(result.items()) == sorted_by_rating
        ), "Result should be sorted by average rating descending"

    def test_top_controversial(self):
        result = self.rating_movies.top_controversial(10)
        assert isinstance(result, dict), "Result should be a dictionary"
        assert all(
            isinstance(title, str) for title in result.keys()
        ), "Movie title should be a string"
        assert all(
            isinstance(avg_rating, float) for avg_rating in result.values()
        ), "Variance of rating should be a float"
        sorted_by_rating = sorted(result.items(), key=lambda x: x[1], reverse=True)
        assert (
            list(result.items()) == sorted_by_rating
        ), "Result should be sorted by variance of rating descending"

    def test_data_movie_id_title(self):
        result = self.rating_movies.data_movie_id_title()
        assert isinstance(result, list), "Result should be a list"

    def test_dist_by_num_of_ratings(self):
        result = self.users.dist_by_num_of_rating()
        assert isinstance(result, dict), "Result should be a dictionary"
        assert all(
            isinstance(title, str) for title in result.keys()
        ), "User id should be a string"
        assert all(
            isinstance(counts, int) for counts in result.values()
        ), "Count of ratings should be a int"
        sorted_by_counts = sorted(result.items(), key=lambda x: x[1], reverse=True)
        assert (
            list(result.items()) == sorted_by_counts
        ), "Result should be sorted by counts of rating descending"

    def test_dist_by_ratings(self):
        result = self.users.dist_by_rating_values()
        assert isinstance(result, dict), "Result should be a dictionary"
        assert all(
            isinstance(title, str) for title in result.keys()
        ), "User id should be a string"
        assert all(
            isinstance(ratings, float) for ratings in result.values()
        ), "Rating should be a float"
        sorted_by_ratings = sorted(result.items(), key=lambda x: x[1], reverse=True)
        assert (
            list(result.items()) == sorted_by_ratings
        ), "Result should be sorted by rating descending"

    def test_top_controversial(self):
        result = self.users.top_controversial_users(5)
        assert isinstance(result, dict), "Result should be a dictionary"
        assert all(
            isinstance(title, str) for title in result.keys()
        ), "User id should be a string"
        assert all(
            isinstance(ratings, float) for ratings in result.values()
        ), "Variance of rating should be a float"
        sorted_by_ratings = sorted(result.items(), key=lambda x: x[1], reverse=True)
        assert (
            list(result.items()) == sorted_by_ratings
        ), "Result should be sorted by variance of rating descending"
