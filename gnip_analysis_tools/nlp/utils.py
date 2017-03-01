"""
This file is a place to store utilities for use with code in
Gnip-Analysis-Pipeline.
"""



try:
    from simple_n_grams.stop_words import StopWords
    stop_words = StopWords()
except ImportError:
    stop_words = []

def token_ok(token, min_token_length = 4, stop_words = stop_words): 
    """ 
    This function is intended to be used to select acceptable tokens
    from a list of text tokens. It is used by helper classes such as
    TokenizedBody defined in gnip_analysis_config.measurements.measurement_base 
    """
    if len(token) < min_token_length:
        return False
    if stop_words[token]:
        return False
    return True

def term_comparator(term1, term2):
    """
    This function normalizes strings for comparison. It is used by
    measurement classes such as SpecifiedBodyTermCounters defined in
    in gnip_analysis_config.measurements.measurement_base  
    """
    t1 = term1.lower().strip(' ').rstrip(' ')
    t2 = term2.lower().strip(' ').rstrip(' ')
    return t1 == t2

def sanitize_string(input_str): 
    """ 
    This function is intended to sanitize the names of counters as returned by
    a measurement's 'get' method. It removes characters that could be interpreted
    as metacharacters by the shell or downstream applications acting on the output CSV.
    
    This function is imported and used by the following measurement base classes:
    Counters 
    GetBase
    """
    output_str = input_str.replace('"','').replace(",","")
    return output_str

