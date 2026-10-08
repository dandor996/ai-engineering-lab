class DomainException(Exception):
    """Base exception for the domain layer"""
    pass

class InvalidPredictionError(DomainException):
    """Exception for invalid prediction inputs"""
    pass

class InvalidFeatureError(DomainException):
    """Exception for invalid feature values"""
    pass

class PredictionTimeoutError(DomainException):
    """Exception for prediction timeout errors"""
    pass