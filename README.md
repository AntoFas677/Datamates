DataMates

DataMates è un gestore di gildani pensato per i giochi MMORPG, sviluppato in Python utilizzando l'interfaccia grafica Tkinter.
Il software consente di gestire in modo intuitivo e ordinato i membri di una gilda, archiviando i loro dati in file JSON dedicati.

In futuro il progetto evolverà in una webapp grazie all'integrazione con Flask o Django.

🔧 Funzionalità principali

Gestione anagrafica dei gildani: Nome, Classe, Ruolo, Data join, Discord, Telegram, Note

Ordinamento della tabella per colonna (alfabetico o per data)

Modifica e cancellazione dei gildani con menu contestuale (tasto destro)

Supporto multi-gilda tramite file JSON separati

Menu "File" per:

Creare una nuova gilda scegliendo il nome

Aprire file JSON esistenti dalla cartella gilde/

Blocco delle funzionalità finché non viene selezionata o creata una gilda

Visualizzazione del nome della gilda attiva nella barra del titolo

📂 Struttura delle cartelle

DataMates/
├── gilde/                 # Contiene i file JSON di ogni gilda
│   ├── LegioneNera.json
│   ├── DraghiDorati.json
│   └── ...
├── DataMates020.py        # Codice principale
├── README.md              # Questo file

🥇 Autore

Sviluppato da AntoFas677 (alias Hawke)

📄 Licenza

Questo progetto è rilasciato sotto licenza MIT.

✨ In futuro

Le prossime funzionalità in programma:

Gestione eventi calendarizzati associati ai gildani

Invio notifiche via Telegram (tramite Bot) ai membri

Risposte agli eventi con "Sì", "No", "Forse" (+ motivazione)

Interfaccia migliorata e porting su web (Flask/Django)

Se ti piace il progetto, lascia una stellina su GitHub e contribuisci allo sviluppo!
