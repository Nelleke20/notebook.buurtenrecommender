import businessrules as rules
import joblib
import logging


class BuurtenModel(rules.BusinessRulesOne, rules.BusinessRulesTwo):
    def __init__(self):
        self._model_one = joblib.load("../data/finalized_model.sav")
        self._model_two = joblib.load("../data/finalized_model.sav")

    def prepare_dataset(self, X):
        logging.info("preparing the dataset...")
        # prepare dataset
        X = X
        return X

    def apply_business_rules_one(self, X):
        # business-rules.py  is used to define business rules
        return super().apply_business_rules_one(X)

    def apply_business_rules_two(self, X, output):
        # business-rules.py  is used to define business rules
        return super().apply_business_rules_two(X, output)

    def apply_model_prediction_one(self, X):
        logging.info("second we will apply the ml-model for the hard-cases...")
        # prediction_type = 'model_voorspelling'
        output = self._model_one.predict(X)
        return output[0]
        # return {'prediction_type_one': prediction_type,
        #         'prediction_one': output[0]}

    def apply_model_prediction_two(
        self,
        X,
    ):
        logging.info("second we will apply the ml-model for the hard-cases...")
        output = self._model_two.predict(X)
        return output[0]

    def predict(self, X):

        # PREP: prepare dataset
        X_prep = self.prepare_dataset(X)

        # PART ONE: apply first business rules and model
        output_step_one = self.apply_business_rules_one(X_prep)
        output_step_one["prediction_one"] = [
            output_step_one["prediction_one"]
            if output_step_one["prediction_type_one"] != "model_voorspelling"
            else self.apply_model_prediction_one(X_prep)
        ]

        # PART TWO: Apply business rules en model for part two
        output_step_two = self.apply_business_rules_two(X_prep, output_step_one)

        output_step_two["prediction_two"] = [
            output_step_two["prediction_two"]
            if output_step_two["prediction_type_two"] != "model_voorspelling"
            else self.apply_model_prediction_one(X_prep)
        ]

        return output_step_two
