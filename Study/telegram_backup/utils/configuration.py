import yaml

class config_extractor:
    def __init__(self) -> None:
        pass

    @staticmethod
    def storeIDHashChannel():
        api_ID = int(input('Enter your API ID: '))
        api_hash = str(input('Enter your API Hash: '))
        channel = str(input('Enter your API Hash: '))
        session = str(input('Enter your session location')) # it might me something like config/<some-name>.session

        config_data = {
            'api_ID': api_ID,
            'api_hash': api_hash,
            'channel': channel,
            'session' : session
        }

        with open('config/config.yaml', 'w') as yaml_file:
            yaml.dump(config_data, yaml_file, default_flow_style=False)

    @staticmethod
    def fetchIDandHash():
        with open('config/config.yaml', 'r') as yaml_file:
            loaded_config = yaml.safe_load(yaml_file)
            return loaded_config['api_ID'], loaded_config['api_hash']

    @staticmethod    
    def fetchIDHashChannel():
        with open('config/config.yaml', 'r') as yaml_file:
            loaded_config = yaml.safe_load(yaml_file)
            return loaded_config['api_ID'], loaded_config['api_hash'], loaded_config['channel']
        
    @staticmethod
    def fetchIDHashChannelSession ():
        with open('config/config.yaml', 'r') as yaml_file:
            loaded_config = yaml.safe_load(yaml_file)
            return loaded_config['api_ID'], loaded_config['api_hash'], loaded_config['channel'], loaded_config['session']
        
if __name__ == '__main__':
    config_extractor.storeIDandHash()
