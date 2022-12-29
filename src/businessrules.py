import logging


class BusinessRules:
    """
    Define business rules to apply to dataframe.

    Attributes:
        X (pd.DataFrame): features that are needed to
        determine if business rules apply to this item.

    """

    def __init__(self):
        pass

    def apply_business_rules(self, X):
        logging.info(
            "first we will apply the business-rules for all the cases (where possible)..."
        )

        # business-rule 1: check if feature one is bigger than
        if X[0][0] > 350:
            prediction_type = 'business rule 1'
            logging.info("based on business rule 1")
            return {'prediction_type': prediction_type,
                    'prediction': 'inboedel'}

        # business-rule 2: check if feature two is bigger than
        elif X[0][1] > 12:
            prediction_type = 'business rule 2'
            logging.info("based on business rule 2")
            return {'prediction_type': prediction_type,
                    'prediction': 'woonhuis'}            

        # when no business-rule is applicable, we pass it to the ML-model
        else:
            logging.info("no business-rule applicable..")
            pass
