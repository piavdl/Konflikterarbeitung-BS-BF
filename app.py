import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ==================================================
# WEB-ANWENDUNG: BARRIEREFREIHEIT / BRANDSCHUTZ
# ==================================================

st.set_page_config(page_title="Gebäudeanalyse Tool", layout="wide")

st.title("🏗️ Digitales Prüftool: Barrierefreiheit & Brandschutz")
st.write("Lade eine Excel-Gebäudeanalyse hoch, um Konflikte zu prüfen und Berichte zu generieren.")

# --------------------------------------------------
# INTERAKTIVER SEITEN-UPLOAD (Ersetzt feste Pfade)
# --------------------------------------------------
uploaded_file = st.file_uploader("1. Excel-Datei auswählen (.xlsx)", type=["xlsx"])

if uploaded_file is not None:
    
    # --------------------------------------------------
    # INTERAKTIVE AUSWAHL (Ersetzt feste Variablen)
    # --------------------------------------------------
    auswahl_bauteil = st.selectbox(
        "2. Für welches Bauteil möchtest du den Detailbericht sehen?",
        ["Tür", "Flur", "Treppe"]
    )
    
    # --------------------------------------------------
    # DEIN CODE: Excel-Datei einlesen und vorbereiten
    # --------------------------------------------------
    # Wir lesen direkt die hochgeladene Datei aus dem Speicher
    df = pd.read_excel(uploaded_file, header=2)

    # Spaltennamen bereinigen
    df.columns = (
        df.columns.astype(str)
        .str.replace("\n", " ", regex=False)
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )

    # Platzhalter als leere Werte behandeln
    df = df.replace(["-", " - ", "--", ""], pd.NA)

    # --------------------------------------------------
    # DEIN CODE: Hilfsfunktion & Zahlen-Spalten erzeugen
    # --------------------------------------------------
    def wert_aus_text(wert):
        if pd.isna(wert): return None
        text = str(wert).strip().lower()
        if text in ["", "-", "--"]: return None
        text = text.replace(" ", "").replace(",", ".")
        if "-" in text:
            text = text.replace("cm", "").replace("m", "")
            teile = text.split("-")
            min_wert, max_wert = float(teile[0]), float(teile[1])
            if min_wert > 5:
                min_wert, max_wert = min_wert / 100, max_wert / 100
            return (min_wert, max_wert)
        text = text.replace("cm", "").replace("m", "")
        zahl = float(text)
        if zahl > 5: zahl = zahl / 100
        return zahl

    # Türen
    df["Türbreite Ist"] = df["Türbreite Ist-Wert"].apply(wert_aus_text)
    df["Türbreite Soll BF"] = df["Türbreite Soll-Wert BF"].apply(wert_aus_text)
    df["Türbreite Soll BS"] = df["Türbreite Soll-Wert BS"].apply(wert_aus_text)
    # Flure
    df["Flurbreite Ist"] = df["Flurbreite Ist-Wert"].apply(wert_aus_text)
    df["Flurbreite Soll BF"] = df["Flurbreite Soll-Wert BF"].apply(wert_aus_text)
    df["Flurbreite Soll BS"] = df["Flurbreite Soll-Wert BS"].apply(wert_aus_text)
    # Treppen
    df["Treppenbreite Ist"] = df["Treppenbreite Ist-Wert"].apply(wert_aus_text)
    df["Treppenbreite Soll BF"] = df["Treppenbreite Soll-Wert BF"].apply(wert_aus_text)
    df["Treppenbreite Soll BS"] = df["Treppenbreite Soll-Wert BS"].apply(wert_aus_text)
    df["Auftrittsmaß Ist"] = df["Stufen Auftrittsmaß Ist-Wert"].apply(wert_aus_text)
    df["Auftrittsmaß Soll BF"] = df["Stufen Auftrittsmaß Soll-Wert BF"].apply(wert_aus_text)
    df["Auftrittsmaß Soll BS"] = df["Stufen Auftrittsmaß Soll-Wert BS"].apply(wert_aus_text)
    df["Steigungsmaß Ist"] = df["Stufen Steigungsmaß Ist-Wert"].apply(wert_aus_text)
    df["Steigungsmaß Soll BF"] = df["Stufen Steigungsmaß Soll-Wert BF"].apply(wert_aus_text)
    df["Steigungsmaß Soll BS"] = df["Stufen Steigungsmaß Soll-Wert BS"].apply(wert_aus_text)

    # --------------------------------------------------
    # DEIN CODE: Regeltabelle & Ampelfunktion
    # --------------------------------------------------
    regeln = [
        {"Bauteil": "Tür", "Kriterium": "Türbreite", "ID-Spalte": "Tür-ID", "Ist-Spalte": "Türbreite Ist", "Soll-BF-Spalte": "Türbreite Soll BF", "Soll-BS-Spalte": "Türbreite Soll BS", "Ist-Anzeige": "Türbreite Ist-Wert", "Soll-BF-Anzeige": "Türbreite Soll-Wert BF", "Soll-BS-Anzeige": "Türbreite Soll-Wert BS", "Mangel-BF": "Türbreite nach Barrierefreiheit zu gering", "Mangel-BS": "Türbreite nach Brandschutz zu gering"},
        {"Bauteil": "Flur", "Kriterium": "Flurbreite", "ID-Spalte": "Raum-ID", "Ist-Spalte": "Flurbreite Ist", "Soll-BF-Spalte": "Flurbreite Soll BF", "Soll-BS-Spalte": "Flurbreite Soll BS", "Ist-Anzeige": "Flurbreite Ist-Wert", "Soll-BF-Anzeige": "Flurbreite Soll-Wert BF", "Soll-BS-Anzeige": "Flurbreite Soll-Wert BS", "Mangel-BF": "Flurbreite nach Barrierefreiheit zu gering", "Mangel-BS": "Flurbreite nach Brandschutz zu gering"},
        {"Bauteil": "Treppe", "Kriterium": "Treppenbreite", "ID-Spalte": "Raum-ID", "Ist-Spalte": "Treppenbreite Ist", "Soll-BF-Spalte": "Treppenbreite Soll BF", "Soll-BS-Spalte": "Treppenbreite Soll BS", "Ist-Anzeige": "Treppenbreite Ist-Wert", "Soll-BF-Anzeige": "Treppenbreite Soll-Wert BF", "Soll-BS-Anzeige": "Treppenbreite Soll-Wert BS", "Mangel-BF": "Mangel Barrierefreiheit", "Mangel-BS": "Mangel Brandschutz"},
        {"Bauteil": "Treppe", "Kriterium": "Auftrittsmaß", "ID-Spalte": "Raum-ID", "Ist-Spalte": "Auftrittsmaß Ist", "Soll-BF-Spalte": "Auftrittsmaß Soll BF", "Soll-BS-Spalte": "Auftrittsmaß Soll BS", "Ist-Anzeige": "Stufen Auftrittsmaß Ist-Wert", "Soll-BF-Anzeige": "Stufen Auftrittsmaß Soll-Wert BF", "Soll-BS-Anzeige": "Stufen Auftrittsmaß Soll-Wert BS", "Mangel-BF": "Mangel Barrierefreiheit", "Mangel-BS": "Mangel Brandschutz"},
        {"Bauteil": "Treppe", "Kriterium": "Steigungsmaß", "ID-Spalte": "Raum-ID", "Ist-Spalte": "Steigungsmaß Ist", "Soll-BF-Spalte": "Steigungsmaß Soll BF", "Soll-BS-Spalte": "Steigungsmaß Soll BS", "Ist-Anzeige": "Stufen Steigungsmaß Ist-Wert", "Soll-BF-Anzeige": "Stufen Steigungsmaß Soll-Wert BF", "Soll-BS-Anzeige": "Stufen Steigungsmaß Soll-Wert BS", "Mangel-BF": "Mangel Barrierefreiheit", "Mangel-BS": "Mangel Brandschutz"}
    ]

    def pruefe_ampel(ist, soll):
        if ist is None or pd.isna(ist) or soll is None or pd.isna(soll): return ""
        if isinstance(soll, tuple):
            soll_min, soll_max = soll
            return "🟢" if soll_min <= ist <= soll_max else "🔴"
        return "🟢" if ist >= soll else "🔴"

    # --------------------------------------------------
    # DEIN CODE: Regeln anwenden & Berichte erzeugen
    # --------------------------------------------------
    alle_ergebnisse = []
    for regel in regeln:
        teil_df = df[df[regel["Ist-Spalte"]].notna()].copy()
        teil_df["Ampel Barrierefreiheit"] = teil_df.apply(lambda r: pruefe_ampel(r[regel["Ist-Spalte"]], r[regel["Soll-BF-Spalte"]]), axis=1)
        teil_df["Ampel Brandschutz"] = teil_df.apply(lambda r: pruefe_ampel(r[regel["Ist-Spalte"]], r[regel["Soll-BS-Spalte"]]), axis=1)

        def konflikttext(row):
            maengel = []
            if row["Ampel Barrierefreiheit"] == "🔴":
                maengel.append(f"{regel['Mangel-BF']} (Kat: {regel['Kriterium']}, Ist: {row[regel['Ist-Anzeige']]}, Soll BF: {row[regel['Soll-BF-Anzeige']]})")
            if row["Ampel Brandschutz"] == "🔴":
                maengel.append(f"{regel['Mangel-BS']} (Kat: {regel['Kriterium']}, Ist: {row[regel['Ist-Anzeige']]}, Soll BS: {row[regel['Soll-BS-Anzeige']]})")
            return " | ".join(maengel)

        teil_df["Konflikt / Mangel"] = teil_df.apply(konflikttext, axis=1)
        
        ergebnis = pd.DataFrame({
            "Geschoss": teil_df["Geschoss"], "Wohneinheit": teil_df["Wohneinheit"], "Raumbez.": teil_df["Raumbez."], "Raum-ID": teil_df["Raum-ID"],
            "Bauteil": regel["Bauteil"], "Bauteil-ID": teil_df[regel["ID-Spalte"]], "Kriterium": regel["Kriterium"], "Ist-Wert": teil_df[regel["Ist-Anzeige"]],
            "Sollwert Barrierefreiheit": teil_df[regel["Soll-BF-Anzeige"]], "Ampel Barrierefreiheit": teil_df["Ampel Barrierefreiheit"],
            "Sollwert Brandschutz": teil_df[regel["Soll-BS-Anzeige"]], "Ampel Brandschutz": teil_df["Ampel Brandschutz"], "Konflikt / Mangel": teil_df["Konflikt / Mangel"]
        })
        alle_ergebnisse.append(ergebnis)

    gesamtbericht = pd.concat(alle_ergebnisse, ignore_index=True)

    def bewertung_aus_ampeln(row):
        BF, BS = row["Ampel Barrierefreiheit"], row["Ampel Brandschutz"]
        if BF == "🟢" and BS == "🟢": return "kein Mangel"
        elif BF == "🔴" and BS == "🟢": return "Mangel Barrierefreiheit"
        elif BF == "🟢" and BS == "🔴": return "Mangel Brandschutz"
        elif BF == "🔴" and BS == "🔴": return "Mangel in Barrierefreiheit und Brandschutz"
        return ""

    gesamtbericht["Ergebnis"] = gesamtbericht.apply(bewertung_aus_ampeln, axis=1)

    # Wohnungsübersicht & Vulnerabilität
    gesamtbericht["Wohnung"] = gesamtbericht["Wohneinheit"].fillna("Treppenhaus")

    def anmerkung_bf(g):
        m = g[g["Ampel Barrierefreiheit"] == "🔴"]["Kriterium"].tolist()
        return ", ".join(m) + " nicht erfüllt" if m else ""
    def anmerkung_bs(g):
        m = g[g["Ampel Brandschutz"] == "🔴"]["Kriterium"].tolist()
        return ", ".join(m) + " nicht erfüllt" if m else ""
    def zusammenfassung_ampel(w):
        w = [x for x in w if x != ""]
        return "🔴" if "🔴" in w else ("🟢" if w else "")
    def gesamtampel(bf, bs):
        if bf == "🔴" and bs == "🔴": return "🔴"
        elif bf == "🔴" or bs == "🔴": return "🟡"
        elif bf == "🟢" and bs == "🟢": return "🟢"
        return ""

    wohnungs_uebersicht = gesamtbericht.groupby(["Wohnung", "Bauteil", "Bauteil-ID"], dropna=False).apply(
        lambda gruppe: pd.Series({"Ampel BF": zusammenfassung_ampel(gruppe["Ampel Barrierefreiheit"]), "Anmerkung BF": anmerkung_bf(gruppe), "Ampel BS": zusammenfassung_ampel(gruppe["Ampel Brandschutz"]), "Anmerkung BS": anmerkung_bs(gruppe)}), include_groups=False
    ).reset_index()

    wohnungs_uebersicht["Ampel Gesamt"] = wohnungs_uebersicht.apply(lambda r: gesamtampel(r["Ampel BF"], r["Ampel BS"]), axis=1)
    wohnungs_uebersicht = wohnungs_uebersicht.rename(columns={"Bauteil": "Kategorie", "Bauteil-ID": "ID"})
    wohnungs_uebersicht = wohnungs_uebersicht[["Wohnung", "Kategorie", "ID", "Ampel BF", "Anmerkung BF", "Ampel BS", "Anmerkung BS", "Ampel Gesamt"]]

    # Vulnerabilitätsindex
    wohnungs_uebersicht_bewertet = wohnungs_uebersicht[wohnungs_uebersicht["Ampel Gesamt"] != ""].copy()
    vulnerabilitaet = wohnungs_uebersicht_bewertet.groupby("Wohnung")["Ampel Gesamt"].value_counts(normalize=True).mul(100).round(1).unstack(fill_value=0).reset_index()
    for spalte in ["🟢", "🟡", "🔴"]:
        if spalte not in vulnerabilitaet.columns: vulnerabilitaet[spalte] = 0
    vulnerabilitaet = vulnerabilitaet[["Wohnung", "🟢", "🟡", "🔴"]].rename(columns={"🟢": "Grün in %", "🟡": "Gelb in %", "🔴": "Rot in %"})
    vulnerabilitaet["Vulnerabilitätsindex"] = (vulnerabilitaet["Gelb in %"] * 1 + vulnerabilitaet["Rot in %"] * 2) / 2

    # Berichte filtern
    bericht = gesamtbericht[gesamtbericht["Bauteil"] == auswahl_bauteil]
    konfliktliste = gesamtbericht[gesamtbericht["Konflikt / Mangel"] != ""][["Geschoss", "Wohneinheit", "Raumbez.", "Raum-ID", "Bauteil", "Bauteil-ID", "Kriterium", "Konflikt / Mangel"]]
    
    # --------------------------------------------------
    # WEB-UI: ERGEBNISSE LIVE ANZEIGEN (Ersetzt Print-Befehle)
    # --------------------------------------------------
    st.header("📊 Auswertung & Kennzahlen")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Geprüfte Elemente (aktiv)", len(bericht))
    col2.metric("Einträge in Konfliktliste", len(konfliktliste))
    col3.metric("Durchschnittl. Vulnerabilität", f"{vulnerabilitaet['Vulnerabilitätsindex'].mean():.1f}")

    # Tabs für bessere Übersicht
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Detailbericht Bauteil", "🚨 Konfliktliste (Alle)", "🏠 Wohnungsübersicht", "📈 Diagramme & Indizes"])

    with tab1:
        st.subheader(f"Detailbericht für Bauteil: {auswahl_bauteil}")
        st.dataframe(bericht)
        # Integrierter Download Button
        st.download_button(f"CSV für {auswahl_bauteil} herunterladen", bericht.to_csv(index=False, sep=";").encode('utf-8-sig'), f"Bericht_{auswahl_bauteil}.csv", "text/csv")

    with tab2:
        st.subheader("Gesamt-Konfliktliste (Alle Mängel)")
        st.dataframe(konfliktliste)
        st.download_button("Ganze Konfliktliste herunterladen", konfliktliste.to_csv(index=False, sep=";").encode('utf-8-sig'), "Konfliktliste_Alle_Bauteile.csv", "text/csv")

    with tab3:
        st.subheader("Übersicht nach Wohneinheiten")
        st.dataframe(wohnungs_uebersicht)
        st.dataframe(vulnerabilitaet)

    with tab4:
        st.subheader("Visualisierungen")
        
        # Grafik 1: Ampelverteilung
        fig1, ax1 = plt.subplots(figsize=(10, 5))
        ax1.bar(vulnerabilitaet["Wohnung"], vulnerabilitaet["Grün in %"], color="green", label="Grün")
        ax1.bar(vulnerabilitaet["Wohnung"], vulnerabilitaet["Gelb in %"], bottom=vulnerabilitaet["Grün in %"], color="gold", label="Gelb")
        ax1.bar(vulnerabilitaet["Wohnung"], vulnerabilitaet["Rot in %"], bottom=vulnerabilitaet["Grün in %"] + vulnerabilitaet["Gelb in %"], color="red", label="Rot")
        ax1.set_ylabel("Anteil [%]")
        ax1.set_title("Ampelverteilung je Wohneinheit")
        plt.xticks(rotation=45)
        ax1.legend()
        st.pyplot(fig1) # Streamlit-Befehl zum Rendern des Diagramms
        
        # Grafik 2: Vulnerabilitätsindex
        fig2, ax2 = plt.subplots(figsize=(10, 5))
        ax2.bar(vulnerabilitaet["Wohnung"], vulnerabilitaet["Vulnerabilitätsindex"], color="gray")
        ax2.set_ylabel("Index")
        ax2.set_title("Vulnerabilitätsindex je Wohneinheit")
        plt.xticks(rotation=45)
        st.pyplot(fig2)

st.info("Bitte lade eine Excel-Datei hoch, um die Analyse zu starten.")