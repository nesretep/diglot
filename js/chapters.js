var books = ["1 Nephi", "2 Nephi","Jacob","Enos","Jarom","Omni","Words of Mormon","Mosiah",	"Alma",	"Helaman",	"3 Nephi",	"4 Nephi",	"Mormon","Ether","Moroni"]; 
var Helaman = ["Chapter1","Chapter2","Chapter3","Chapter4","Chapter5","Chapter6","Chapter7","Chapter8","Chapter9","Chapter10","Chapter11","Chapter12","Chapter13","Chapter14","Chapter15","Chapter16"];
var BOM ={
	"1 Nephi": ["Chapter 1","Chapter 2","Chapter 3","Chapter 4","Chapter 5","Chapter 6","Chapter 7","Chapter 8","Chapter 9","Chapter 10","Chapter 11","Chapter 12","Chapter 13","Chapter 14","Chapter 15","Chapter 16","Chapter 17","Chapter 18","Chapter 19","Chapter 20","Chapter 21","Chapter 22"],
	"2 Nephi": ["Chapter 1","Chapter 2","Chapter 3","Chapter 4","Chapter 5","Chapter 6","Chapter 7","Chapter 8","Chapter 9","Chapter 10","Chapter 11","Chapter 12","Chapter 13","Chapter 14","Chapter 15","Chapter 16","Chapter 17","Chapter 18","Chapter 19","Chapter 20","Chapter 21","Chapter 22","Chapter 23","Chapter 24","Chapter 25","Chapter 26","Chapter 27","Chapter 28","Chapter 29","Chapter 30","Chapter 31","Chapter 32","Chapter 33"],
	"Jacob": ["Chapter 1", "Chapter 2", "Chapter 3", "Chapter 4", "Chapter 5","Chapter 6","Chapter 7"],
	"Enos": ["Chapter 1"],
	"Jarom": ["Chapter 1"],
	"Omni": ["Chapter 1"],
	"Words of Mormon": ["Chapter 1"],
	"Mosiah": ["Chapter 1","Chapter 2","Chapter 3","Chapter 4","Chapter 5","Chapter 6","Chapter 7","Chapter 8","Chapter 9","Chapter 10","Chapter 11","Chapter 12","Chapter 13","Chapter 14","Chapter 15","Chapter 16","Chapter 17","Chapter 18","Chapter 19","Chapter 20","Chapter 21","Chapter 22","Chapter 23","Chapter 24","Chapter 25","Chapter 26","Chapter 27","Chapter 28","Chapter 29"],
	"Alma": ["Chapter 1","Chapter 2","Chapter 3","Chapter 4","Chapter 5","Chapter 6","Chapter 7","Chapter 8","Chapter 9","Chapter 10","Chapter 11","Chapter 12","Chapter 13","Chapter 14","Chapter 15","Chapter 16","Chapter 17","Chapter 18","Chapter 19","Chapter 20","Chapter 21","Chapter 22","Chapter 23","Chapter 24","Chapter 25","Chapter 26","Chapter 27","Chapter 28","Chapter 29","Chapter 30","Chapter 31","Chapter 32","Chapter 33","Chapter 34","Chapter 35","Chapter 36","Chapter 37","Chapter 38","Chapter 39","Chapter 40","Chapter 41","Chapter 42","Chapter 43","Chapter 44","Chapter 45","Chapter 46","Chapter 47","Chapter 48","Chapter 49","Chapter 50","Chapter 51","Chapter 52","Chapter 53","Chapter 54","Chapter 55","Chapter 56","Chapter 57","Chapter 58","Chapter 59","Chapter 60","Chapter 61","Chapter 62","Chapter 63"],
	"Helaman": ["Chapter 1","Chapter 2","Chapter 3","Chapter 4","Chapter 5","Chapter 6","Chapter 7","Chapter 8","Chapter 9","Chapter 10","Chapter 11","Chapter 12","Chapter 13","Chapter 14","Chapter 15","Chapter 16"],
	"3 Nephi": ["Chapter 1","Chapter 2","Chapter 3","Chapter 4","Chapter 5","Chapter 6","Chapter 7","Chapter 8","Chapter 9","Chapter 10","Chapter 11","Chapter 12","Chapter 13","Chapter 14","Chapter 15","Chapter 16","Chapter 17","Chapter 18","Chapter 19","Chapter 20","Chapter21","Chapter 22","Chapter 23","Chapter 24","Chapter 25","Chapter 26","Chapter 27","Chapter 28","Chapter 29","Chapter 30"],
	"4 Nephi": ["Chapter 1"],
	"Mormon": ["Chapter 1", "Chapter 2", "Chapter 3", "Chapter 4", "Chapter 5","Chapter 6","Chapter 7","Chapter 8","Chapter 9"],
	"Ether": ["Chapter 1","Chapter 2","Chapter 3","Chapter 4","Chapter 5","Chapter 6","Chapter 7","Chapter 8","Chapter 9","Chapter 10","Chapter 11","Chapter 12","Chapter 13","Chapter 14","Chapter 15"],
	"Moroni": ["Chapter 1", "Chapter 2", "Chapter 3", "Chapter 4", "Chapter 5","Chapter 6","Chapter 7","Chapter 8","Chapter 9","Chapter 10"]
}

new Vue({
       el: '#BookOfMormon',
       data: {
       	   books,
           BOM,
           "Active_Chapter" : "1 Nephi"
       }
})

