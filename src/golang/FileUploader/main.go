package main

import (
	"flag"
	"io"
	"log"
	"net/http"
	"os"
	"time"
)

type filesHandlerArgs struct {
	FileFormName string
	Directory    string
}

func (fh *filesHandlerArgs) uploadFile(w http.ResponseWriter, r *http.Request) {
	log.Printf("File Upload Endpoint Hit")

	// Parse request body as multipart form data with 32MB max memory
	err := r.ParseMultipartForm(32 << 20)
	if err != nil {
		log.Fatalf(err.Error())
	}

	// Get file uploaded via Form
	file, handler, err := r.FormFile(fh.FileFormName)
	if err != nil {
		log.Fatalf(err.Error())
	}
	defer file.Close()

	// Create file locally
	dst, err := os.Create(fh.Directory + handler.Filename)
	if err != nil {
		log.Fatalf(err.Error())
	}
	defer dst.Close()

	// Copy the uploaded file data to the newly created file on the filesystem
	if _, err := io.Copy(dst, file); err != nil {
		log.Fatalf(err.Error())
	}

	http.Redirect(w, r, "/", http.StatusSeeOther)

	log.Printf("Successfully Uploaded File\n")
}

func main() {
	log.Printf("Start FileUploader")
	var frontend, fileformname, directory string

	flag.StringVar(&frontend, "frontend", "static", "Static folder for frontend")
	flag.StringVar(&fileformname, "form-input-name", "file", "Name of input type file at form")
	flag.StringVar(&directory, "directory", "data", "Directory to save files")
	flag.Parse()

	filesHandler := &filesHandlerArgs{
		FileFormName: fileformname,
		Directory:    directory + "/",
	}

	mux := http.NewServeMux()

	mux.Handle(
		"/",
		http.FileServer(http.Dir(frontend)),
	)

	mux.HandleFunc(
		"/upload",
		filesHandler.uploadFile,
	)

	s := &http.Server{
		Addr:           ":8080",
		Handler:        mux,
		ReadTimeout:    10 * time.Second,
		WriteTimeout:   10 * time.Second,
		MaxHeaderBytes: 1 << 20,
	}
	if err := s.ListenAndServe(); err != nil {
		log.Fatalf("server failed to start with error %v", err.Error())
	}

}
