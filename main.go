// forms.go
package main

import (
    "html/template"
    "net/http"
    "fmt"
    "encoding/csv"
    "os"
    "time"
    "os/exec"
)

type ContactDetails struct {
    plate	string
    vehicle_type	string
    waste_type	string
    commercial	string
}
type Daily struct {
    rainfall	string
    waste_bins	string
    comingled_bins	string
    cardboard_bins	string
    comments	string
}
type Weekly struct {
    scrap_wetal	string
    green_waste	string
    batteries	string
    oil	string
    generator_fuel string
    generator_started string
}

type Monthly struct{
	fire_extinguisher string
	first_aid	string
	septic_level string
	water_tank string
}



func main() {
	http.HandleFunc("/daily/", daily)
	http.HandleFunc("/new_visitor/", new_visitor)
	http.HandleFunc("/generate", generate)
	http.Handle("/reports/", http.StripPrefix("/reports/", http.FileServer(http.Dir("./reports"))))
	http.HandleFunc("/", main_page)
	fmt.Println("Listening and Serving")
    http.ListenAndServe(":8999", nil)
    
}

func main_page(w http.ResponseWriter, r *http.Request){
	
	tmpl := template.Must(template.ParseFiles("index.html"))
	if r.Method != http.MethodPost {
            tmpl.Execute(w, nil)
            return
        }
	}

func generate(w http.ResponseWriter, r *http.Request){
	fmt.Println("Generating reports")
	cmd := exec.Command("python3", "generate-spreadsheet.py")
out, err := cmd.Output()

if err != nil {
    println(err.Error())
    return
}

fmt.Println(string(out))
	tmpl := template.Must(template.ParseFiles("generate.html"))
	
	if r.Method != http.MethodPost {
            tmpl.Execute(w, nil)
            return
        }
	}


func daily(w http.ResponseWriter, r *http.Request) {
	tmpl := template.Must(template.ParseFiles("daily.html"))
	if r.Method != http.MethodPost {
            tmpl.Execute(w, nil)
            return
        }

        details := Daily{
            rainfall:   r.FormValue("rainfall"),
            waste_bins: r.FormValue("waste_bins"),
            comingled_bins: r.FormValue("comingled_bins"),
            cardboard_bins: r.FormValue("cardboard_bins"),
            comments: r.FormValue("comments"),
        }

        // do something with details
        fmt.Println(details)
        var f, err = os.OpenFile("daily.csv", os.O_APPEND|os.O_CREATE, 0755)
        if err!=nil{
			fmt.Println(err)
			}
		writer := csv.NewWriter(f)
		dt:=time.Now()
		var data = [][]string{
        {dt.Format("02-01-2006"), details.rainfall, details.waste_bins, details.comingled_bins, details.cardboard_bins, details.comments},
    }
    writer.WriteAll(data)
    f.Close()
        
        tmpl.Execute(w, struct{ Success bool }{true})
    }



func new_visitor(w http.ResponseWriter, r *http.Request) {
	tmpl := template.Must(template.ParseFiles("visitor.html"))
	if r.Method != http.MethodPost {
            tmpl.Execute(w, nil)
            return
        }

        details := ContactDetails{
            plate:   r.FormValue("plate"),
            vehicle_type: r.FormValue("vehicle_type"),
            waste_type: r.FormValue("waste_type"),
            commercial: r.FormValue("commercial"),
        }

        // do something with details

        var f, err = os.OpenFile("visitors.csv", os.O_RDWR, 0777)
        if err!=nil{
			fmt.Println(err)
			}
		writer := csv.NewWriter(f)
		dt:=time.Now()
		var data = [][]string{
        {dt.Format("02-01-2006"), dt.Format("15:04:05"), details.plate, details.vehicle_type, details.waste_type, details.commercial},
    }
    fmt.Println(data)
    writer.WriteAll(data)
    f.Close()
        
        tmpl.Execute(w, struct{ Success bool }{true})
    }
