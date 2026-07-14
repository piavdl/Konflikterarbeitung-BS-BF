# ==================================================
# DIGITALE AUSWERTUNG BARRIEREFREIHEIT / BRANDSCHUTZ
# ==================================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re 
# JETZT NEU: Absicherung gegen Matplotlib-Abstürze (Segmentation Faults)
from matplotlib.backends.backend_agg import RendererAgg
_lock = RendererAgg.lock
def pruefe_passwort():
    """Gibt True zurück, wenn das Passwort korrekt ist."""
    if "authentifiziert" not in st.session_state:
        st.session_state["authentifiziert"] = False

    if st.session_state["authentifiziert"]:
        return True

    # Login-Formular anzeigen
    st.markdown("<h2 style='color:#00549F;'>🔒 Geschützter Bereich</h2>", unsafe_allow_html=True)
    st.info("Dieses Prüftool ist im Rahmen eines universitären Projekts geschützt. Bitte gib das Passwort ein.")
    
    passwort = st.text_input("Passwort eingeben:", type="password")
    
    if st.button("Anmelden"):
        if passwort == "IPE_2026": # <-- Hier dein Wunschpasswort eintragen
            st.session_state["authentifiziert"] = True
            st.rerun()
        else:
            st.error("❌ Falsches Passwort. Bitte versuche es erneut.")
            
    return False

# Erst das Passwort prüfen. Wenn falsch, stoppt das Skript hier.
if not pruefe_passwort():
    st.stop()

# Streamlit Seiten-Konfiguration (Muss ganz oben stehen)
st.set_page_config(
    page_title="Digitale Auswertung Barrierefreiheit & Brandschutz",
    layout="wide"
)

st.title("🏢 Prüftool: Barrierefreiheit & Brandschutz")
st.markdown("Lade deine Excel-Gebäudeanalyse hoch, um Berichte, Mängellisten und den Vulnerabilitätsindex live auszuwerten.")

# --------------------------------------------------
# 1. Interaktive Steuerung direkt in der Mitte
# --------------------------------------------------

# Das Upload-Feld prominent in der Mitte
hochgeladene_datei = st.file_uploader(
    "1. Bitte lade hier deine Excel-Gebäudeanalyse hoch:", 
    type=["xlsx"]
)

# Die Bauteilauswahl direkt darunter in der Mitte
auswahl_bauteil = st.selectbox(
    "2. Für welches Bauteil möchtest du den Detailbericht sehen?",
    ["Tür", "Flur", "Treppe", "Handlauf", "Rauchmelder", "Leitsystem"]
)

st.markdown("---") # Trennlinie für eine saubere Optik

# --------------------------------------------------
# 3. Hilfsfunktion: Werte aus Excel umwandeln
# --------------------------------------------------
def wert_aus_text(wert):
    if pd.isna(wert):
        return None

    text = str(wert).strip().lower()

    if text in ["", "-", "--"]:
        return None

    text = text.replace(" ", "")
    text = text.replace(",", ".")

    # Bereich, z. B. 26-37cm
    if "-" in text:
        text = text.replace("cm", "").replace("m", "")
        teile = text.split("-")

        min_wert = float(teile[0])
        max_wert = float(teile[1])

        if min_wert > 5:
            min_wert = min_wert / 100
            max_wert = max_wert / 100

        return (min_wert, max_wert)

    # Einzelwert
    text = text.replace("cm", "").replace("m", "")
    try:
        zahl = float(text)
        if zahl > 5:
            zahl = zahl / 100
        return zahl
    except ValueError:
        return None

def pruefe_ampel(ist, soll):
    if ist is None or pd.isna(ist):
        return ""
    if soll is None:
        return ""
    if isinstance(soll, tuple):
        soll_min, soll_max = soll
        if soll_min <= ist <= soll_max:
            return "🟢"
        return "🔴"
    if pd.isna(soll):
        return ""
    if ist >= soll:
        return "🟢"
    return "🔴"

def pruefe_ja_nein(wert):
    if pd.isna(wert):
        return ""
    if wert == 1:
        return "🟢"
    if wert == 0:
        return "🔴"
    return ""

# Erst ausführen, wenn auch wirklich eine Datei hochgeladen wurde
if hochgeladene_datei is not None:
    # --------------------------------------------------
    # 2. Excel-Datei einlesen und vorbereiten (Robust & Speicherschonend)
    # --------------------------------------------------
    df = pd.read_excel(hochgeladene_datei, header=2)
    
    # JETZT NEU: Löscht alle Zeilen, die komplett leer sind (Phantom-Zeilen vom Excel-Export)
    # Es müssen Daten in 'Geschoss' vorhanden sein, sonst fliegt die Zeile radikal raus.
    if "Geschoss" in df.columns:
        df = df.dropna(subset=["Geschoss"], how="all")
    else:
        df = df.dropna(how="all")

    # Spaltennamen bereinigen (mit dem re.sub-Fix für die doppelten Leerzeichen bei Türen/Fluren)
    df.columns = [re.sub(r'\s+', ' ', str(c)).strip() for c in df.columns]

    # Platzhalter als leere Werte behandeln (Speicherschonend ohne Absturz!)
    for col in df.columns:
        df[col] = df[col].astype(str).replace(["-", " - ", "--", "", "nan", "None"], None)

    # --------------------------------------------------
    # 4. Zahlen-Spalten erzeugen
    # --------------------------------------------------
    # Türen
    if "Türbreite Ist-Wert" in df.columns:
        df["Türbreite Ist"] = df["Türbreite Ist-Wert"].apply(wert_aus_text)
        df["Türbreite Soll BF"] = df["Türbreite Soll-Wert BF"].apply(wert_aus_text)
        df["Türbreite Soll BS"] = df["Türbreite Soll-Wert BS"].apply(wert_aus_text)

    # Flure
    if "Flurbreite Ist-Wert" in df.columns:
        df["Flurbreite Ist"] = df["Flurbreite Ist-Wert"].apply(wert_aus_text)
        df["Flurbreite Soll BF"] = df["Flurbreite Soll-Wert BF"].apply(wert_aus_text)
        df["Flurbreite Soll BS"] = df["Flurbreite Soll-Wert BS"].apply(wert_aus_text)

    # Treppen
    if "Treppenbreite Ist-Wert" in df.columns:
        df["Treppenbreite Ist"] = df["Treppenbreite Ist-Wert"].apply(wert_aus_text)
        df["Treppenbreite Soll BF"] = df["Treppenbreite Soll-Wert BF"].apply(wert_aus_text)
        df["Treppenbreite Soll BS"] = df["Treppenbreite Soll-Wert BS"].apply(wert_aus_text)
        df["Auftrittsmaß Ist"] = df["Stufen Auftrittsmaß Ist-Wert"].apply(wert_aus_text)
        df["Auftrittsmaß Soll BF"] = df["Stufen Auftrittsmaß Soll-Wert BF"].apply(wert_aus_text)
        df["Auftrittsmaß Soll BS"] = df["Stufen Auftrittsmaß Soll-Wert BS"].apply(wert_aus_text)
        df["Steigungsmaß Ist"] = df["Stufen Steigungsmaß Ist-Wert"].apply(wert_aus_text)
        df["Steigungsmaß Soll BF"] = df["Stufen Steigungsmaß Soll-Wert BF"].apply(wert_aus_text)
        df["Steigungsmaß Soll BS"] = df["Stufen Steigungsmaß Soll-Wert BS"].apply(wert_aus_text)

    # Handläufe
    if "Anzahl Handläufe Ist-Wert" in df.columns:
        df["Anzahl Handläufe Ist"] = pd.to_numeric(df["Anzahl Handläufe Ist-Wert"], errors="coerce")
        df["Anzahl Handläufe Soll"] = pd.to_numeric(df["Anzahl Handläufe Soll-Wert"], errors="coerce")
        df["Höhe Handlauf Ist"] = df["Höhe Handlauf Ist-Wert"].apply(wert_aus_text)
        df["Höhe Handlauf Soll BF"] = df["Höhe Handlauf Soll-Wert BF"].apply(wert_aus_text)
        df["Höhe Handlauf Soll BS"] = df["Höhe Handlauf Soll-Wert BS"].apply(wert_aus_text)

    # Rauchmelder und Leitsystem
    if "Rauchmelder" in df.columns:
        df["Rauchmelder Ist"] = pd.to_numeric(df["Rauchmelder"], errors="coerce")
    if "Leitsystem" in df.columns:
        df["Leitsystem Ist"] = pd.to_numeric(df["Leitsystem"], errors="coerce")

    # --------------------------------------------------
    # 5. Regeltabelle
    # --------------------------------------------------
    regeln = [
        {"Bauteil": "Tür", "Kriterium": "Türbreite", "ID-Spalte": "Tür-ID", "Ist-Spalte": "Türbreite Ist", "Soll-BF-Spalte": "Türbreite Soll BF", "Soll-BS-Spalte": "Türbreite Soll BS", "Ist-Anzeige": "Türbreite Ist-Wert", "Soll-BF-Anzeige": "Türbreite Soll-Wert BF", "Soll-BS-Anzeige": "Türbreite Soll-Wert BS", "Mangel-BF": "Türbreite nach Barrierefreiheit zu gering", "Mangel-BS": "Türbreite nach Brandschutz zu gering", "Pruefart": "vergleich"},
        {"Bauteil": "Flur", "Kriterium": "Flurbreite", "ID-Spalte": "Raum-ID", "Ist-Spalte": "Flurbreite Ist", "Soll-BF-Spalte": "Flurbreite Soll BF", "Soll-BS-Spalte": "Flurbreite Soll BS", "Ist-Anzeige": "Flurbreite Ist-Wert", "Soll-BF-Anzeige": "Flurbreite Soll-Wert BF", "Soll-BS-Anzeige": "Flurbreite Soll-Wert BS", "Mangel-BF": "Flurbreite nach Barrierefreiheit zu gering", "Mangel-BS": "Flurbreite nach Brandschutz zu gering", "Pruefart": "vergleich"},
        {"Bauteil": "Treppe", "Kriterium": "Treppenbreite", "ID-Spalte": "Raum-ID", "Ist-Spalte": "Treppenbreite Ist", "Soll-BF-Spalte": "Treppenbreite Soll BF", "Soll-BS-Spalte": "Treppenbreite Soll BS", "Ist-Anzeige": "Treppenbreite Ist-Wert", "Soll-BF-Anzeige": "Treppenbreite Soll-Wert BF", "Soll-BS-Anzeige": "Treppenbreite Soll-Wert BS", "Mangel-BF": "Mangel Barrierefreiheit", "Mangel-BS": "Mangel Brandschutz", "Pruefart": "vergleich"},
        {"Bauteil": "Treppe", "Kriterium": "Auftrittsmaß", "ID-Spalte": "Raum-ID", "Ist-Spalte": "Auftrittsmaß Ist", "Soll-BF-Spalte": "Auftrittsmaß Soll BF", "Soll-BS-Spalte": "Auftrittsmaß Soll BS", "Ist-Anzeige": "Stufen Auftrittsmaß Ist-Wert", "Soll-BF-Anzeige": "Stufen Auftrittsmaß Soll-Wert BF", "Soll-BS-Anzeige": "Stufen Auftrittsmaß Soll-Wert BS", "Mangel-BF": "Mangel Barrierefreiheit", "Mangel-BS": "Mangel Brandschutz", "Pruefart": "vergleich"},
        {"Bauteil": "Treppe", "Kriterium": "Steigungsmaß", "ID-Spalte": "Raum-ID", "Ist-Spalte": "Steigungsmaß Ist", "Soll-BF-Spalte": "Steigungsmaß Soll BF", "Soll-BS-Spalte": "Steigungsmaß Soll BS", "Ist-Anzeige": "Stufen Steigungsmaß Ist-Wert", "Soll-BF-Anzeige": "Stufen Steigungsmaß Soll-Wert BF", "Soll-BS-Anzeige": "Stufen Steigungsmaß Soll-Wert BS", "Mangel-BF": "Mangel Barrierefreiheit", "Mangel-BS": "Mangel Brandschutz", "Pruefart": "vergleich"},
        {"Bauteil": "Handlauf", "Kriterium": "Anzahl Handläufe", "ID-Spalte": "Raum-ID", "Ist-Spalte": "Anzahl Handläufe Ist", "Soll-BF-Spalte": "Anzahl Handläufe Soll", "Soll-BS-Spalte": "Anzahl Handläufe Soll", "Ist-Anzeige": "Anzahl Handläufe Ist-Wert", "Soll-BF-Anzeige": "Anzahl Handläufe Soll-Wert", "Soll-BS-Anzeige": "Anzahl Handläufe Soll-Wert", "Mangel-BF": "Zu wenige Handläufe", "Mangel-BS": "Zu wenige Handläufe", "Pruefart": "vergleich"},
        {"Bauteil": "Handlauf", "Kriterium": "Höhe Handlauf", "ID-Spalte": "Raum-ID", "Ist-Spalte": "Höhe Handlauf Ist", "Soll-BF-Spalte": "Höhe Handlauf Soll BF", "Soll-BS-Spalte": "Höhe Handlauf Soll BS", "Ist-Anzeige": "Höhe Handlauf Ist-Wert", "Soll-BF-Anzeige": "Höhe Handlauf Soll-Wert BF", "Soll-BS-Anzeige": "Höhe Handlauf Soll-Wert BS", "Mangel-BF": "Handlaufhöhe nicht ausreichend", "Mangel-BS": "Handlaufhöhe nicht ausreichend", "Pruefart": "vergleich"},
        {"Bauteil": "Rauchmelder", "Kriterium": "Rauchmelder vorhanden", "ID-Spalte": "Raum-ID", "Ist-Spalte": "Rauchmelder Ist", "Soll-BF-Spalte": None, "Soll-BS-Spalte": None, "Ist-Anzeige": "Rauchmelder", "Soll-BF-Anzeige": None, "Soll-BS-Anzeige": None, "Mangel-BF": "Rauchmelder nicht vorhanden", "Mangel-BS": "Rauchmelder nicht vorhanden", "Pruefart": "ja_nein"},
        {"Bauteil": "Leitsystem", "Kriterium": "Leitsystem vorhanden", "ID-Spalte": "Raum-ID", "Ist-Spalte": "Leitsystem Ist", "Soll-BF-Spalte": None, "Soll-BS-Spalte": None, "Ist-Anzeige": "Leitsystem", "Soll-BF-Anzeige": None, "Soll-BS-Anzeige": None, "Mangel-BF": "Leitsystem nicht vorhanden", "Mangel-BS": "Leitsystem nicht vorhanden", "Pruefart": "ja_nein"}
    ]

    # --------------------------------------------------
    # 7. Regeln anwenden
    # --------------------------------------------------
    alle_ergebnisse = []

    for regel in regeln:
        if regel["Ist-Spalte"] not in df.columns:
            continue
            
        teil_df = df[df[regel["Ist-Spalte"]].notna()].copy()
        if teil_df.empty:
            continue

        if regel.get("Pruefart") == "ja_nein":
            teil_df["Ampel Barrierefreiheit"] = teil_df[regel["Ist-Spalte"]].apply(pruefe_ja_nein)
            teil_df["Ampel Brandschutz"] = teil_df[regel["Ist-Spalte"]].apply(pruefe_ja_nein)
        else:
            teil_df["Ampel Barrierefreiheit"] = teil_df.apply(lambda row: pruefe_ampel(row[regel["Ist-Spalte"]], row[regel["Soll-BF-Spalte"]]), axis=1)
            teil_df["Ampel Brandschutz"] = teil_df.apply(lambda row: pruefe_ampel(row[regel["Ist-Spalte"]], row[regel["Soll-BS-Spalte"]]), axis=1)

        def konflikttext(row):
            maengel = []
            if row["Ampel Barrierefreiheit"] == "🔴":
                text = f"{regel['Mangel-BF']} (Kategorie: {regel['Kriterium']}, Ist: {row[regel['Ist-Anzeige']]}"
                if regel["Soll-BF-Anzeige"] is not None:
                    text += f", Soll BF: {row[regel['Soll-BF-Anzeige']]}"
                text += ")"
                maengel.append(text)

            if row["Ampel Brandschutz"] == "🔴":
                text = f"{regel['Mangel-BS']} (Kategorie: {regel['Kriterium']}, Ist: {row[regel['Ist-Anzeige']]}"
                if regel["Soll-BS-Anzeige"] is not None:
                    text += f", Soll BS: {row[regel['Soll-BS-Anzeige']]}"
                text += ")"
                maengel.append(text)
            return " | ".join(maengel)

        teil_df["Konflikt / Mangel"] = teil_df.apply(konflikttext, axis=1)

        soll_bf_anzeige = teil_df[regel["Soll-BF-Anzeige"]] if regel["Soll-BF-Anzeige"] is not None else ""
        soll_bs_anzeige = teil_df[regel["Soll-BS-Anzeige"]] if regel["Soll-BS-Anzeige"] is not None else ""

        ergebnis = pd.DataFrame({
            "Geschoss": teil_df["Geschoss"],
            "Wohneinheit": teil_df["Wohneinheit"],
            "Raumbez.": teil_df["Raumbez."],
            "Raum-ID": teil_df["Raum-ID"],
            "Bauteil": regel["Bauteil"],
            "Bauteil-ID": teil_df[regel["ID-Spalte"]],
            "Kriterium": regel["Kriterium"],
            "Ist-Wert": teil_df[regel["Ist-Anzeige"]],
            "Sollwert Barrierefreiheit": soll_bf_anzeige,
            "Ampel Barrierefreiheit": teil_df["Ampel Barrierefreiheit"],
            "Sollwert Brandschutz": soll_bs_anzeige,
            "Ampel Brandschutz": teil_df["Ampel Brandschutz"],
            "Konflikt / Mangel": teil_df["Konflikt / Mangel"]
        })
        alle_ergebnisse.append(ergebnis)

    if alle_ergebnisse:
        gesamtbericht = pd.concat(alle_ergebnisse, ignore_index=True)
        
        # --------------------------------------------------
        # 9. Ergebnis aus BF- und BS-Ampel ableiten
        # --------------------------------------------------
        def bewertung_aus_ampeln(row):
            BF = row["Ampel Barrierefreiheit"]
            BS = row["Ampel Brandschutz"]
            if BF == "🟢" and BS == "🟢": return "kein Mangel"
            elif BF == "🔴" and BS == "🟢": return "Mangel Barrierefreiheit"
            elif BF == "🟢" and BS == "🔴": return "Mangel Brandschutz"
            elif BF == "🔴" and BS == "🔴": return "Mangel in Barrierefreiheit und Brandschutz"
            return ""

        gesamtbericht["Ergebnis"] = gesamtbericht.apply(bewertung_aus_ampeln, axis=1)
        gesamtbericht["Wohnung"] = gesamtbericht["Wohneinheit"].fillna("Treppenhaus")

        # --------------------------------------------------
        # 10. Wohnungsübersicht & Index erstellen
        # --------------------------------------------------
        wohnungs_uebersicht = (
            gesamtbericht
            .groupby(["Wohnung", "Bauteil", "Bauteil-ID"], dropna=False)
            .agg({
                "Ampel Barrierefreiheit": lambda x: "🔴" if "🔴" in list(x) else ("🟢" if "🟢" in list(x) else ""),
                "Ampel Brandschutz": lambda x: "🔴" if "🔴" in list(x) else ("🟢" if "🟢" in list(x) else ""),
                "Kriterium": lambda x: ", ".join(x.dropna().astype(str).unique())
            })
            .reset_index()
        )

        wohnungs_uebersicht = wohnungs_uebersicht.rename(columns={
            "Bauteil": "Kategorie", "Bauteil-ID": "ID", "Ampel Barrierefreiheit": "Ampel BF", "Ampel Brandschutz": "Ampel BS", "Kriterium": "Kriterien"
        })

        def gesamtampel(bf, bs):
            if bf == "🔴" and bs == "🔴": return "🔴"
            elif bf == "🔴" or bs == "🔴": return "🟡"
            elif bf == "🟢" and bs == "🟢": return "🟢"
            return ""

        wohnungs_uebersicht["Ampel Gesamt"] = wohnungs_uebersicht.apply(lambda row: gesamtampel(row["Ampel BF"], row["Ampel BS"]), axis=1)

        wohnungs_uebersicht_bewertet = wohnungs_uebersicht[wohnungs_uebersicht["Ampel Gesamt"] != ""].copy()
        vulnerabilitaet = (
            wohnungs_uebersicht_bewertet
            .groupby("Wohnung")["Ampel Gesamt"]
            .value_counts(normalize=True)
            .mul(100)
            .round(1)
            .unstack(fill_value=0)
            .reset_index()
        )

        for spalte in ["🟢", "🟡", "🔴"]:
            if spalte not in vulnerabilitaet.columns:
                vulnerabilitaet[spalte] = 0

        vulnerabilitaet = vulnerabilitaet[["Wohnung", "🟢", "🟡", "🔴"]].rename(columns={"🟢": "Grün in %", "🟡": "Gelb in %", "🔴": "Rot in %"})
        vulnerabilitaet["Vulnerabilitätsindex"] = (vulnerabilitaet["Gelb in %"] * 1 + vulnerabilitaet["Rot in %"] * 2) / 2

        # --------------------------------------------------
        # Web-Oberfläche strukturieren (Tabs)
        # --------------------------------------------------
        tab1, tab2, tab3 = st.tabs(["📊 Dashboard & Indizes", "🔍 Detailbericht & Fazit", "⚠️ Komplette Mängelliste"])

        with tab1:
            st.header("Gebäude-Vulnerabilität und Ampelverteilung")
            
            # Kennzahlen im Überblick
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Vulnerabilitätsindex je Wohneinheit")
                st.dataframe(vulnerabilitaet, use_container_width=True)
            
            with col2:
                # Diagramm 1: Ampelverteilung (Sicher verpackt gegen Abstürze)
                with _lock:
                    fig1, ax1 = plt.subplots(figsize=(6, 4))
                    ax1.bar(vulnerabilitaet["Wohnung"], vulnerabilitaet["Grün in %"], color="green", label="Grün")
                    ax1.bar(vulnerabilitaet["Wohnung"], vulnerabilitaet["Gelb in %"], bottom=vulnerabilitaet["Grün in %"], color="gold", label="Gelb")
                    ax1.bar(vulnerabilitaet["Wohnung"], vulnerabilitaet["Rot in %"], bottom=vulnerabilitaet["Grün in %"] + vulnerabilitaet["Gelb in %"], color="red", label="Rot")
                    ax1.set_ylabel("Anteil [%]")
                    ax1.set_title("Ampelverteilung je Wohneinheit")
                    plt.xticks(rotation=45)
                    ax1.set_ylim(0, 100)
                    ax1.legend(loc="upper right")
                    st.pyplot(fig1)

            # Diagramm 2: Vulnerabilitätsindex (Sicher verpackt gegen Abstürze)
            st.subheader("Visualisierung Vulnerabilitätsindex")
            with _lock:
                fig2, ax2 = plt.subplots(figsize=(10, 3))
                ax2.bar(vulnerabilitaet["Wohnung"], vulnerabilitaet["Vulnerabilitätsindex"], color="gray")
                ax2.set_ylabel("Index-Wert")
                plt.xticks(rotation=45)
                st.pyplot(fig2)

        with tab2:
            st.header(f"Detailanalyse: {auswahl_bauteil}")
            
            bericht = gesamtbericht[gesamtbericht["Bauteil"] == auswahl_bauteil]
            anzahl = len(bericht)
            bf_gruen = (bericht["Ampel Barrierefreiheit"] == "🟢").sum()
            bf_rot = (bericht["Ampel Barrierefreiheit"] == "🔴").sum()
            bs_gruen = (bericht["Ampel Brandschutz"] == "🟢").sum()
            bs_rot = (bericht["Ampel Brandschutz"] == "🔴").sum()

            fazit = pd.DataFrame({
                "Kennzahl": ["Geprüfte Elemente", "Barrierefreiheit erfüllt", "Barrierefreiheit nicht erfüllt", "Brandschutz erfüllt", "Brandschutz nicht erfüllt"],
                "Anzahl": [anzahl, bf_gruen, bf_rot, bs_gruen, bs_rot]
            })

            col_f1, col_f2 = st.columns([1, 2])
            with col_f1:
                st.subheader("Statistisches Fazit")
                st.dataframe(fazit, use_container_width=True)
            with col_f2:
                st.subheader("Gefilterte Bauteildaten")
                st.dataframe(bericht, use_container_width=True)

        with tab3:
            st.header("Gesamte Konflikt- und Mängelliste")
            konfliktliste = gesamtbericht[gesamtbericht["Konflikt / Mangel"] != ""][
                ["Geschoss", "Wohneinheit", "Raumbez.", "Raum-ID", "Bauteil", "Bauteil-ID", "Kriterium", "Konflikt / Mangel"]
            ]
            if not konfliktliste.empty:
                st.error(f"Achtung: Es wurden {len(konfliktliste)} Mängel im Gebäude identifiziert.")
                st.dataframe(konfliktliste, use_container_width=True)
            else:
                st.success("Hervorragend! Es wurden keine Konflikte oder Mängel gefunden.")

else:
    st.info("💡 Bitte lade die Excel-Datei 'GebaeudeanalyseV1.xlsx' in der linken Seitenleiste hoch, um die Auswertung zu starten.")
