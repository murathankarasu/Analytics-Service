from app import create_app

app = create_app()

if __name__ == '__main__':
    print("Flask uygulaması başlatılıyor...")
    print("http://localhost:8000 adresinde çalışıyor")
    app.run(debug=True, host='0.0.0.0', port=8000)
