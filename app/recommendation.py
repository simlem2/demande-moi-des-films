# coding: utf-8

# All the recommandation logic and algorithms goes here

from random import choice

from app.User import User


class Recommendation:

    def __init__(self, movielens):

        # Dictionary of movies
        # The structure of a movie is the following:
        #     * id (which is the movie number, you can access to the movie with "self.movies[movie_id]")
        #     * title
        #     * release_date (year when the movie first aired)
        #     * adventure (=1 if the movie is about an adventure, =0 otherwise)
        #     * drama (=1 if the movie is about a drama, =0 otherwise)
        #     * ... (the list of genres)
        self.movies = movielens.movies

        # List of ratings
        # The structure of a rating is the following:
        #     * movie (with the movie number)
        #     * user (with the user number)
        #     * is_appreciated (in the case of simplified rating, whether or not the user liked the movie)
        #     * score (in the case of rating, the score given by the user)
        self.ratings = movielens.simplified_ratings

        # This is the set of users in the training set
        self.test_users = {}

        # Launch the process of ratings
        self.process_ratings_to_users()

    # To process ratings, users associated to ratings are created and every rating is then stored in its user
    def process_ratings_to_users(self):
        for rating in self.ratings:
            user = self.register_test_user(rating.user)
            movie = self.movies[rating.movie]
            if hasattr(rating, 'is_appreciated'):
                if rating.is_appreciated:
                    user.good_ratings.append(movie)
                else:
                    user.bad_ratings.append(movie)
            if hasattr(rating, 'score'):
                user.ratings[movie.id] = rating.score

    # Register a user if it does not exist and return it
    def register_test_user(self, sender):
        if sender not in self.test_users.keys():
            self.test_users[sender] = User(sender)
        return self.test_users[sender]

    # Display the recommendation for a user
    def make_recommendation(self, user):
        similarities = self.compute_all_similarities(user)
        max_simi = 0
        user_max = User(0)
        for u, s in similarities.items():
            if s > max_simi:
                max_simi = s
                user_max = u
        movie = choice(Recommendation.get_user_appreciated_movies(user_max)).title
        return "Vos recommandations : " + ", ".join([movie])

    # Compute the similarity between two users
    @staticmethod
    def get_similarity(user_a, user_b):
        scal = 0
        for elm in user_a.good_ratings:
            if elm in user_b.good_ratings:
                scal += 3
            elif elm in user_b.bad_ratings:
                scal += 1
        for elm in user_a.bad_ratings:
            if elm in user_b.good_ratings:
                scal += 1
            elif elm in user_b.bad_ratings:
                scal += 3
        min_both = min(Recommendation.get_user_norm(user_a), Recommendation.get_user_norm(user_b))
        return scal/min_both

    # Compute the similarity between a user and all the users in the data set
    def compute_all_similarities(self, user):
        tab = {}
        for other_user in self.test_users.values():
            tab[other_user] = Recommendation.get_similarity(user, other_user)
        return tab

    @staticmethod
    def get_best_movies_from_users(users):
        return []

    @staticmethod
    def get_user_appreciated_movies(user):
        return user.good_ratings

    @staticmethod
    def get_user_norm(user):
        somme = len(user.good_ratings) + len(user.bad_ratings)
        return somme

    # Return a vector with the normalised ratings of a user
    @staticmethod
    def get_normalised_cluster_notations(user):
        return []
