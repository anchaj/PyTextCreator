
def print_notification_form():
    global result
    result = MutableString()

    result.append('<form method="POST">')
    result.append('<h1>Generowanie zawiadomienia</h1>')

    result.append('<span>Dane geodety:</span><br>')
    result.append('<span>Imię: </span><input type="text" name="name" value="' + 'textname' + '"/><br>')
    result.append('<span>Nazwisko: </span><input type="text" name="surname" value="' + 'textname' + '"/><br>')
    result.append('<span>NIP: </span><input type="text" name="nip" value="' + 'textname' + '"/><br>')
    result.append('<span>REGON: </span><input type="text" name="regon" value="' + 'textname' + '"/><br>')
    result.append('<span>Dane geodety - adres:</span><br>')
    result.append('<span>Ulica: </span><input type="text" name="street" value="' + 'textname' + '"/><br>')
    result.append('<span>Numer domu: </span><input type="text" name="number" value="' + 'textname' + '"/><br>')
    result.append('<span>Miejscowość: </span><input type="text" name="place" value="' + 'textname' + '"/><br>')
    result.append('<span>Kod pocztowy: </span><input type="text" name="postcode" value="' + 'textname' + '"/><br>')

    result.append('<span>Tytuł: </span><input type="text" name="subtitle" value="' + 'textname' + '"/><br>')
    result.append('<span>Treść:</span>')
    result.append('<textarea rows = "10" cols = "100" name="content">')
    result.append('texttext')
    result.append('</textarea>')
    result.append('<input type="hidden" name="doc_type" value="notification_rewrite"/>')
    result.append('<input type="submit" value="Generuj zawiadomienie"/>')

    result.append('</form>')

    return result


def print_protocol_form():
    global result
    result = MutableString()

    result.append('<form method="POST">')
    result.append('<h1>Generowanie protokołu</h1>')

    result.append('<span>Województwo: </span><input type="text" name="voivodeship"/><br>')
    result.append('<span>Powiat: </span><input type="text" name="powiat"/><br>')
    result.append('<span>Jednostka ewidencyjna: </span><input type="text" name="registry_unit"/><br>')
    result.append('<span>Nazwa jednostki: </span><input type="text" name="precinct_name"/><br>')
    result.append('<span>Numer jednostki: </span><input type="text" name="precinct_number"/><br>')
    result.append('<span>Tytuł protokołu: </span><input type="text" name="title"/><br>')
    result.append('<span>Opis protokołu: </span><input type="text" name="subtitle"/><br>')
    result.append('<span>Liczba kolumn tabeli: </span><input type="text" name="columns"/><br>')
    result.append('<span>Tabela:</span>')
    result.append('<textarea rows = "10" cols = "100" name="content">')
    result.append('</textarea>')
    result.append('<input type="hidden" name="doc_type" value="protocol_submit"/>')
    result.append('<input type="submit" value="Generuj protokół"/>')

    result.append('</form>')

    return result
