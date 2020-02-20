#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <netinet/in.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <sys/stat.h>
#include <errno.h>
#include <sys/stat.h> 
#include <fcntl.h>


#define errno 0


int BUF_SIZE = 512;

int WinnerSend(int conn){
    struct stat fileWinner;
    int sent_bytes = 0;
    int remain_data;
    int offset = 0;
    int test;
    long fileSize;
    char symbol;
    char buffer[BUF_SIZE];
    char filename[12];
    strcpy(filename,"./Winner.pdf");
    
    FILE *fp = fopen(filename, "r");
    fstat(filename, &fileWinner);
    if(fp == -1){
        char errtxt[100];
        perror(errtxt);
        printf("%s \n", errtxt);
        return 1;
    }

    if(stat(filename, &fileWinner) == -1){
        char errtxt[100];
        perror(errtxt);
        printf("%s \n", errtxt);
        return 1;
    }

    remain_data = fileWinner.st_size;
    //przesyłanie rozmiaru pliku
    fileSize = fileWinner.st_size;
    printf("iloś” bitów = %d  zawartość = %d\n", sizeof(fileSize), fileSize);
    test = send(conn, &fileSize, sizeof(fileSize), 0);

     if(test == -1){
        char errtxt[100];
        perror(errtxt);
        printf("%s \n", errtxt);
        return 1;
    }

    //przesyłanie pliku
    while (remain_data > 0){
        if(remain_data >= 512){
            fread(buffer, 1, BUF_SIZE, fp);
            sent_bytes = send(conn, buffer, BUF_SIZE, 0);
        }
        else{
            fread(buffer, 1, remain_data, fp);
            sent_bytes = send(conn, buffer, remain_data, 0);
        }
            if(sent_bytes == -1){
                char errtxt[100];
                perror(errtxt);
                printf("%s \n", errtxt);
                return 1;
            }
            remain_data -= sent_bytes;
            printf("Przesłano %d bytów, Pozostało: %d \n", sent_bytes,remain_data);
    }

    if(sent_bytes == -1){
        char errtxt[100];
        perror(errtxt);
        printf("%s \n", errtxt);
        return 1;
    }

    printf("Przesłano: %d bytów \n", sent_bytes);
    fclose(fp);
    return 0;
}



int main(int argc, char **argv)
{
    struct sockaddr_in myaddr1, endpoint1, endpoint2, myaddr2;
    int sdsocket1, sdconnection1, addrlen1, sdsocket2, sdconnection2, addrlen2;
    int s = 0;
    int r = 0;
    int check = 2;
    char res[2];
    char fleet1[10][3];
    char fleet2[10][3];
    char test[2];
    char fleetTest[2];
    char gameTest[2];
    int fleetCounter1 = 10;
    int fleetCounter2 = 10;
    int winnerNumber = 0;
    strcpy(res,"ck");
    
    if (argc < 2) {
        printf("podaj numer portu jako parametr\n");
        return 1;
    }
    printf("Czekanie na graczy \n");
    sdsocket1 = socket(AF_INET, SOCK_STREAM, 0);
    sdsocket2 = socket(AF_INET, SOCK_STREAM, 0);
    addrlen1 = sizeof(struct sockaddr_in);
    addrlen2 = sizeof(struct sockaddr_in);

    myaddr1.sin_family = AF_INET;
    myaddr1.sin_port = htons(atoi(argv[1]));
    myaddr1.sin_addr.s_addr = htonl(INADDR_ANY);

    myaddr2.sin_family = AF_INET;
    myaddr2.sin_port = htons(atoi(argv[1]));
    myaddr2.sin_addr.s_addr = htonl(INADDR_ANY);


    if (bind(sdsocket1,(struct sockaddr*) &myaddr1,addrlen1) < 0) {
        printf("bind() numer 1 nie powiodl sie\n");
        return 1;
    }


    if (listen(sdsocket1, 10) < 0) {
        printf("listen() numer1 nie powiodl sie\n");
        return 1;
    }

    //rozrusznik i połączenie P1
    sdconnection1 = accept(sdsocket1, (struct sockaddr*) &endpoint1, &addrlen1);
    strcpy(res,"p1");
    s = send(sdconnection1, res, sizeof(res), 0);
    printf("%d \n",s);
    if (s != sizeof(res)) {
        printf("send nie powiodl sie (send failed)\n");
        close(sdconnection1);
    }
    else
    {
        printf("Gracz nr.1 rozstawia wojska \n");
    }

    //odbiór danych o flocie P1
    for(int l = 0;l<10;l++){
        r = recv(sdconnection1, fleetTest, sizeof(fleetTest),0);

        if (r != sizeof(fleetTest)) {
            printf("recv nie powiodl sie (recv failed)\n");
            close(sdconnection1);
            return -1;
        }
        strcpy(fleet1[l],fleetTest);
        printf("%d:Odebrano: %d bajtów \n",l,r);
        printf("%d:Zawartość: %s \n",l,fleetTest);
        printf("%d:Wojska ustawiona na pozycji: %s \n",l,fleet1[l]);
    }
    
   // rozrusznik i połączenie P2
    sdconnection2 = accept(sdsocket1, (struct sockaddr*) &endpoint2, &addrlen2); 
    strcpy(res,"p2");
    s = send(sdconnection2, res, sizeof(res), 0);
    printf("%d \n",s);
    if (s != sizeof(res)) {
        printf("send nie powiodl sie (send failed)\n");
        close(sdconnection2);
    }
    else
    {
        printf("Gracz nr.2 rozstawia wojska \n");
    }
    //odbiór danych o flocie P2
    for(int l = 0;l<10;l++){
        r = recv(sdconnection2, fleetTest, sizeof(fleetTest),0);

        if (r != sizeof(fleetTest)) {
            printf("recv nie powiodl sie (recv failed)\n");
            close(sdconnection2);
            return -1;
        }
        strcpy(fleet2[l],fleetTest);
        printf("%d:Odebrano: %d bajtów\n",l,r);
        printf("%d:Zawartość: %s \n",l,fleetTest);
        printf("%d:Wojska ustawiona na pozycji: %s \n",l,fleet2[l]);
    }
     printf("Start! \n");
    //printf("%d \n",WinnerSend(sdconnection1));

    //RUNDA
    while (1){
        printf("Kolejna runda \n");

        //recive from p1
        printf("Strzela gracz nr.1 \n");
         r = recv(sdconnection1, gameTest, sizeof(test),0);

        if (r != sizeof(gameTest)) {
            printf("recv nie powiodl sie (recv failed)\n");
            close(sdconnection1);
            break;
        }
        printf("1:Odebrano: %d bajtów\n",r);
        printf("1:Zawartość: %s \n",gameTest);

        //analiza strzału p1
        check = 0;
        for(int i = 0; i < 10; i++){
            printf("%s \n",fleet2[i]);
            if(strcmp(gameTest,fleet2[i])==0){
                fleetCounter2--;
                printf("Trafiony, graczowi nr2 pozostało %d statków\n",fleetCounter2);
                strcpy(fleet2[i],"ff");
                check = 1;
                break;
            }
            else{
                printf("Nie trafiony, pozostało graczowi nr2 pozostało %d statków\n",fleetCounter2);
                continue;
            }
        }
        //Określanie zwycięzcy nr.1
        if(fleetCounter2 == 0){
            printf("WYGRAŁ GRACZ NUMER 1\n");
            winnerNumber = 1;
            strcpy(res,"w1");
            send(sdconnection1, res, sizeof(res), 0);
            send(sdconnection2, res, sizeof(res), 0);
            break;
        }
        else if(check == 0){
            strcpy(res,"no");
        }
        else if(check == 1){
            strcpy(res,"ok");
        }


        //przesył wyniku p1 
        s = send(sdconnection1, res, sizeof(res), 0);
        printf("Nadano: %d bajtów do P1\n",s);
        if (s != sizeof(res)) {
            printf("send do p1 nie powiodl sie (send failed)\n");
            close(sdconnection1);
            break;
        }
        s = send(sdconnection2, res, sizeof(res), 0);
        printf("Nadano: %d bajtów do P2\n",s);
        if (s != sizeof(res)) {
            printf("send do p2 nie powiodl sie (send failed)\n");
            close(sdconnection2);
            break;
        }
       
        //recive from p2
        printf("Strzela gracz nr.2 \n");
         r = recv(sdconnection2, gameTest, sizeof(gameTest),0);

        if (r != sizeof(gameTest)) {
            printf("recv od p2 nie powiodl sie (recv failed)\n");
            close(sdconnection2);
            break;
        }
        printf("2:Odebrano: %d bajtów\n",r);
        printf("2:Zawartość: %s \n",gameTest);

        //analiza strzału p2
        check = 0;
        for(int i = 0; i < 10; i++){
            printf("%s \n",fleet1[i]);
            if(strcmp(gameTest,fleet1[i])==0){
                fleetCounter1 --;
                printf("Trafiony, pozostało graczowi nr1 pozostało %d statków\n",fleetCounter1);
                strcpy(fleet1[i],"ff");
                check = 1;
                break;
            }
            else{
                printf("Nie trafiony, pozostało graczowi nr1 pozostało %d statków\n",fleetCounter2);
                continue;
            }
        }

        //Określanie zwycięzcy nr.2
        if(fleetCounter1 == 0){
            printf("WYGRAŁ GRACZ NUMER 2\n");
            winnerNumber = 2;
            strcpy(res,"w2");
            send(sdconnection1, res, sizeof(res), 0);
            send(sdconnection2, res, sizeof(res), 0);
            break;
        }
        else if(check == 0){
                strcpy(res,"no");
        }
        else if(check == 1){
                strcpy(res,"ok");
        }

        //przesył wyniku p2
        s = send(sdconnection2, res, sizeof(res), 0);
        printf("Nadano: %d bajtów do P2\n",s);
        if (s != sizeof(res)) {
            printf("send p2 nie powiodl sie (send failed)\n");
            close(sdconnection2);
            break;
        }
        s = send(sdconnection1, res, sizeof(res), 0);
        printf("Nadano: %d bajtów do P1\n",s);
        if (s != sizeof(res)) {
            printf("send p1 nie powiodl sie (send failed)\n");
            close(sdconnection1);
            break;
        }

    }

    if(winnerNumber == 1){
        WinnerSend(sdconnection1);
    }
    else if(winnerNumber == 2){
        WinnerSend(sdconnection2);
    }
    else{
        printf("Nastąpił błąd przy okreslaniu zwycięzcy \n");
    }
    
    close(sdconnection1);
    close(sdconnection2);
    close(sdsocket1);
    return 0;
}