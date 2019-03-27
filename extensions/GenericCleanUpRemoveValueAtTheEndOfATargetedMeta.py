# Title: Generic Clean-Up - Remove value at the end of a targeted meta
# Description: Get that value outta here!
# Required data:
# Parameters: targeted_metadata_name, removeValueAndWhatFollows

def get_safe_meta_data(meta_data_name):
	safe_meta = ''
	meta_data_value = document.get_meta_data_value(meta_data_name)
	if len(meta_data_value) > 0:
		safe_meta = meta_data_value[-1]
	return safe_meta

def removeThisAndWhatFollows(targeted_metadata_name, removeValueAndWhatFollows):
  try:
      targeted_meta = get_safe_meta_data(targeted_metadata_name)
      
      remove_value_position = targeted_meta.find(removeValueAndWhatFollows)

      if remove_value_position > -1:
          updated_meta = targeted_meta[0:remove_value_position]
          document.add_meta_data({targeted_metadata_name: updated_meta})

  except Exception as e:
      log(str(e), 'Error')
      
if 'targeted_metadata_name' not in parameters:
    log('targeted_metadata_name has not been specified, please supply a parameter targeted_metadata_name')
    raise Exception('Supply a targeted_metadata_name in the parameters of ext')
if 'removeValueAndWhatFollows' not in parameters:
    log('removeValueAndWhatFollows has not been specified, please supply a parameter removeValueAndWhatFollows')
    raise Exception('Supply a removeValueAndWhatFollows in the parameters of ext')
    
removeThisAndWhatFollows(parameters['targeted_metadata_name'],parameters['removeValueAndWhatFollows'])