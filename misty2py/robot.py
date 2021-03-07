"""The main script for the misty2py package.
"""
from misty2py.information import *
from misty2py.action import *
from misty2py.utils import *

class Misty:
    """A class representing a Misty robot.

    Attributes
    ----------
    ip : str
        The IP address of this Misty robot.
    infos : Info()
        The object of Info class that belongs to this Misty.
    actions : Action()
        The object of Action class that belongs to this Misty.
    """

    def __init__(self, ip: str, custom_info={}, custom_actions={}, custom_data={}) -> None:
        """Initialises an instance of a Misty robot.

        Parameters
        ----------
        ip : str
            The IP address of this Misty robot.
        custom_info : dict, optional
            Custom information keywords in the form of dictionary with key being the keyword and value being the API endpoint, by default {}
        custom_actions : dict, optional
            Custom actions keywords in the form of dictionary with key being the keyword and value being the API endpoint, by default {}
        custom_data : dict, optional
            Custom data shortcuts in the form of dictionary with key being the shortcut and value being the json data in the form of a dictionary, by default {}
        """
        self.ip = ip
        self.infos = Info(ip, custom_allowed_infos=custom_info)
        self.actions = Action(ip, custom_allowed_actions=custom_actions, custom_allowed_data=custom_data)
        
    def __str__(self) -> str:
        """Transforms a Misty() object into a string.

        Returns
        -------
        str
            A string identifiyng this Misty robot.
        """
        return "A Misty II robot with IP address %s" % self.ip

    def perform_action(self, action_name: str, data = {}) -> bool:
        """Sends Misty a request to perform an action.

        Parameters
        ----------
        action_name : str
            The keyword specifying the action to perform.
        data : str or dict, optional
            The data to send in the request body in the form of a data shortcut or a json dictionary, by default {}

        Returns
        -------
        dict
            response from the API
        """
        if action_name == "led_trans" and isinstance(data, dict) and len(data)>=2 and len(data)<=4:
            try:
                data = construct_transition_dict(data, self.actions.allowed_data)
            except:
                return {"result" : "Failed", "message" : "Data not in correct format."}

        data_method = ""
        if isinstance(data, dict):
            data_method = "dict"
        else:
            data_method = "string"
        r = self.actions.perform_action(action_name, data, data_method)
        return r

    def get_info(self, info_name: str, params: dict = {}) -> dict:
        """Obtains information from Misty.

        Args:
            info_name (str): The information keyword specifying which kind of information to retrieve.
            params (dict): dict of parameter name and parameter value. Defaults to {}.

        Returns:
            dict: The requested information in the form of a json dictionary.
        """
        r = self.infos.get_info(info_name, params)
        return r
