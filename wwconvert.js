
function loadFileToTextarea(files, dstid) {
    /* Take an imported file and place its data in #csvfile on load
     */
    for (var i = 0, numFiles = files.length; i < numFiles; i++) {
        var file = files[i];

        var reader = new FileReader();
        reader.onload = (function(aParent) { return function(e) {
            aParent.value = e.target.result;
        }; })(document.getElementById(dstid));
        reader.readAsText(file);
    }
}

function athenaFullnameToLastname(fullname) {
    /* Given fullname Lastname, Firstname, M., return the student's last
       name, usually "Lastname" */
    return fullname.split(",")[0];
}

function ugaEmailToUsername(email) {
    /* Given a UGA email "myid@uga.edu", return myid. We are probably
       guaranteed not to have any "\@" or other confusing characters. */
    return email.split("@")[0];
}

function convertAthenaCSV(data) {
    /* Parse CSV into list of {password, lastname, firstname, myid},
       one per student, for conversion to WebWork format

       First row of Athena CSV file is header row
       Important columns of Athena CSV file are (0-indexed):
       1: Preferred first name; we use this as firstname
       2: Last, First, M.; we grab up to the comma as lastname
       3: UGA ID; we use this as password
       9: Email in fmt [username]@uga.edu; grepped appropriately */

    var res = Papa.parse(data, {skipEmptyLines: true});
    var students = new Array();

    // First row is header information, which we don't need
    for (var i = 1, numStudents = res.data.length;
         i < numStudents; i++) {
        students.push({
            password: res.data[i][3],
            lastname: athenaFullnameToLastname(res.data[i][2]),
            firstname: res.data[i][1],
            username: ugaEmailToUsername(res.data[i][9]),
        });
    }

    return students;
}

function convertStudentsToWW(students) {
    /* Given a list of dicts with keys password, lastname, firstname,
       username, return a valid row for WebWork lst import. If data is
       incomplete, return None. */
    var wwdata = new Array();
    for (var i = 0, numStudents = students.length;
         i < numStudents; i++) {
        var student = students[i];
        wwdata.push([
            student.password,
            student.lastname,
            student.firstname,
            "C",
            "", "", "", "\t"+student.username+"@uga.edu",
            student.username
        ].join(","));
    }

    return wwdata.join("\n");
}

function convertData(srcid, dstid) {
    /* Take data in #csvdata, convert it, and place it in #lstdata */
    var data = document.getElementById(srcid).value;

    students = convertAthenaCSV(data);
    lststr = convertStudentsToWW(students);

    document.getElementById(dstid).value = lststr;
}
