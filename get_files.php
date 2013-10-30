<?php

define('DISPLAY_HIDDEN_FILESDIRS', FALSE);
define('BASE_URL','/mybaseurl');
define('DOWNLOADS_DIR_URL',BASE_URL.'/downloads'); //

/**
 * Récupère récursivement le contenu d'un répertoire
 * et le retourne sous forme d'array
 * @param $directory Le répertoire à traiter
 **/
function recursive_directory_tree($directory = null) {
	
	$listof_dir=array();
	$excluded_files=array('srt','sfv','nzb','srr','jpg','gif','png','bmp');
	
	//If $directory is null, set $directory to the current working directory.
	if ($directory == null) {
		$directory = getcwd();
	}
	
	//declare the array to return
	$resultat = array();
	
	//Check if the argument specified is an array
	if (is_dir($directory) ) {
		
		array_push($listof_dir,$directory);
		
		//Scan the directory and loop through the results
		foreach(scandir($directory) as $file) {
			
			//. = current directory, .. = up one level. We want to ignore both.
			if ($file[0] == "." && !DISPLAY_HIDDEN_FILESDIRS) {
				continue;
			}
			
			if (in_array(substr(strrchr($file,'.'),1), $excluded_files)) {//Exclude some specified file extensions
				continue;
			}
			
			//Check if the current $file is a directory itself.
			//The appending of $directory is necessary here.
			if (is_dir($directory."/".$file)) {//Create a new array with an index of the folder name.
				$resultat[DOWNLOADS_DIR_URL.'/'.rawurlencode($file)] = recursive_directory_tree($directory."/".$file);
			}
			else {//If $file is not a directory, just add it to the return array.
				$resultat[] = $file;
			}
		}

	}
	else {
		$resultat[] = $directory;
	}
	
	// Detruit les cles dont les valeurs sont vides
	foreach ($resultat as $key => $value) {
		
		if (empty($value)) {
			unset($resultat[$key]);
		}

	}

	// Tri du tableau
	ksort($resultat);
	
	return $resultat;
}

$files = recursive_directory_tree('/home/user/downloads');
echo json_encode($files,JSON_PRETTY_PRINT);