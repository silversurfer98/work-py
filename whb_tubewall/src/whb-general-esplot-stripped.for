	PROGRAM WHBGENERAL
C
C     This program calculates the temperature profile in a boiler.
C     Essentially, it performs the same calculation as the GIPS program
C     HEATEX87 but allows the user to choose how to apply the fouling
C     The input should be taken from a HEATEX simulation and the output
C     for a clean exchanger should be compared with the corresponding
C     profile from HEATEX
C
C     WRITTEN BY SGT - modified Dec 2105 to make input more user friend-
C     ly
C
      REAL*8  T(1),TINLET, X0, XF, STEP
      REAL*8  TI, TM1, TM2, TCHECK, TMEAN, UALL
      REAL*8  TOLD,UOLD,CAPO,DX,QTIL,QAVG,QTOT
      REAL*8  TLI, TLO, FLUX
      real*8  X,BETA
      REAL*8  TG1,CP1,DCP,HI1,DHI,HO1,DHO
      REAL*8  TMEANS
      REAL*8  DI, DO, PI, TW, RL, HI, HO, MPRIK, CAP
      REAL*8  FOUL1, FOUL2

      INTEGER NINT, NPR, NVAR, I, KODE

      CHARACTER*1 ANS
      CHARACTER*72 LINE
C
      COMMON /ONE/ DI, DO, PI, TW, RL, HI, HO, MPRIK, CAP,
     *             FOUL1, FOUL2
      COMMON /FIVE/ TG1,CP1,DCP,HI1,DHI,HO1,DHO

C
C     Open output files to save simulation data and enable plotting
C

      OPEN(10,FILE='OUTPUT1.DAT')
      OPEN(11,FILE='TEMPERATUREPROFILE.TXT')
C
C     Set up problem
C     Number of steps in Runge-Kutta method is 100
C     Every NPR is printed
C
      CALL INITDATA(NINT,NPR,XF)

      X0     = 0.0D0
      STEP   = (XF-X0)/(NINT*NPR)
      NVAR   = 1
      DX     = NINT*STEP
	
      write(11,'(25a)') '$ WALL TEMPERATURE PROFILE '

      WRITE(11,'(A14,F6.4,A12,F6.4)')
     1    '! SHELL FOUL= ',FOUL2,' TUBE FOUL= ',FOUL1

      T(1)   = TG1
      TI     = T(1)

      CALL EVAL(X0,TI,TM1,TM2,TMEAN,TLI,TLO,UALL)
      CALL EVALQ(TI,TOLD,UALL,UOLD,CAPO,DX,QTIL,QAVG,1)
      QTOT = 0.0D0
	
      WRITE(6,*)  '  X   T GAS     TTT     TTS   TMEAN     TLI',
     *     '     TLO   U ALL   FLUX'
      WRITE(10,*) '  X   T GAS     TTT     TTS   TMEAN     TLI',
     *     '     TLO   U ALL   FLUX'
      FLUX = UALL*(T(1)-TW)
      WRITE(6,90) X0,T(1),TM1,TM2,TMEAN,TLI,TLO,UALL,FLUX
      WRITE(10,90) X0,T(1),TM1,TM2,TMEAN,TLI,TLO,UALL,FLUX
      WRITE(11,*) X0,TM1
C   
      TMEANS = 0.0D0
      DO 10 I = 1,NPR
	  CALL RUNKUT(X0,T,NVAR,STEP,NINT)
	  TI = T(1)
	  FLUX = UALL*(TI-TW)
	  CALL EVAL(X0,TI,TM1,TM2,TMEAN,TLI,TLO,UALL)
	  CALL EVALQ(TI,TOLD,UALL,UOLD,CAPO,DX,QTIL,QAVG,2)
	  QTOT = QTOT + QTIL 
	  WRITE(6,90) X0,T(1),TM1,TM2,TMEAN,TLI,TLO,UALL,FLUX
	  WRITE(10,90) X0,T(1),TM1,TM2,TMEAN,TLI,TLO,UALL,FLUX,QTIL,QAVG
	  WRITE(11,*) X0,TM1
	  IF (I .EQ. 1) THEN
	    TMEANS = TMEAN*0.5D0
	  ELSE
	    TMEANS = TMEANS + TMEAN
	  ENDIF

   10 CONTINUE

      WRITE(6,*) ' TRANSFERRED HEAT: ',QTOT,' KCAL'
      WRITE(10,*) ' TRANSFERRED HEAT: ',QTOT,' KCAL'

      WRITE(6,*) ' AVERAGE WALL TEMPERATURE ', TMEANS/19
      WRITE(6,*) ' FOULING FACTOR INSIDE   = ', FOUL1
      WRITE(6,*) ' FOULING FACTOR, OUTSIDE = ', FOUL2
      CLOSE(10)
      CLOSE(11)
C
C PLOT - FIRST REDEFINE TITLE - then call executable file ESPLOT
C
C      OPEN(12,FILE='TUBEWALLTEMP.QTP')
C      OPEN(13,FILE='TUBEWALLMASTER.QTP',STATUS='OLD')
C      DO 40 I = 1,50
C        READ(13,'(72A)',END=41) LINE
C        IF (I .NE. 28) THEN
C          WRITE(12,'(72A)') LINE
C        ELSE
C        WRITE(12,'(A12,F6.4,A12,F6.4)')
C     1    'SHELL FOUL= ',FOUL2,' TUBE FOUL= ',FOUL1
C        END IF
C   40 CONTINUE
C   41 CLOSE(12)
C      CLOSE(13)
C      CALL SYSTEM('ESPLOT TEMPERATUREPROFILE.TXT TUBEWALLTEMP.QTP')
C
C Stop
C
      ANS = 'Y'
      DO WHILE (ANS .NE. 'Y' .AND. ANS .NE. 'y')
        WRITE (6,*) ' STOP Y/N?'
        READ(5,*) ANS
        WRITE(6,*) ANS
      ENDDO
      STOP
   90 FORMAT(F5.3,1X,7(F7.2,1X),E9.3,2(1X,E9.3))
   
      END
      SUBROUTINE INITDATA(NINT,NPR,XF)
C
C       INITALIZE DATA BY READING INPUT FILE
C       NBR OF TUBES, TUBE GEOMETRI, LENGTH AND CONDUCTIVITY
C       FLOW IN TUBE
C       WATER TEMPERATURE
C
C       PRINTOUT AND INTEGRATION FREQUENCIES
C       TITLE IN OUTPUT FILE AND GIPS CALC NUMBER
C
C	DEFINE FOR INLET AND OUTLET (from GIPS calculation)
C	HEAT CAPACITY (kcal/kmol �C)
C       TUBE SIDE FILM COEFFICIENTYS
C       SHELL SIDE FILM COEFFICIENTS
C
C       ADITIONALLY DEFINE:
C	DENSITY (kg/cu.m)
C	VISCOSITY (cP & Kg/m hr)
C	MOLECULAR WEIGHT (kg/kmol)
C	GAS TEMPERATURES (�C)
C
C       ADD FOULING FACTORS, DEFAULT IS ZERO
C       DEFINE OPTIONAL LINER, GAP AND HEAT TRANSFER ENHANCEMENT IN
C       INLET
C
      REAL*8  DI, DO, PI, TW, RL, HI, HO, MPRIK, CAP
      REAL*8  FOUL1, FOUL2
      REAL*8  DILIN,DOLIN,RLINE, DIGAP, DOGAP, RGAP
      REAL*8  TLINER, TGAP
      REAL*8  W, RHO1, RMY1, QVOL, VQ, RE1, DII
      REAL*8  TG1,TG2,CP1,CP2,HI1,HI2,HO1,HO2
      REAL*8  DCP,DHI,DHO,DTG
      REAL*8  A1,V1
      REAL*8  XF
      INTEGER NINT,NPR,NTUB,NGIPS
      CHARACTER*80 HEADING
      CHARACTER*12 COMMAND
      LOGICAL LINER, GAP,INLET
C
      COMMON /ONE/ DI, DO, PI, TW, RL, HI, HO, MPRIK, CAP,
     *             FOUL1, FOUL2
      COMMON /TWO/ DILIN,DOLIN,RLINE,LINER,INLET
      COMMON /THREE/ DIGAP,DOGAP,RGAP,GAP
      COMMON /FOUR/ RE1, DII
      COMMON /FIVE/ TG1,CP1,DCP,HI1,DHI,HO1,DHO
      COMMON /SIX/  NGIPS,HEADING

      PI    = 2.0D0*ASIN(1.0D0)
C
C       Open input file and start parsing commands until EOF
C
      OPEN(14,FILE='INPUT.TXT',STATUS='OLD',ERR=100)
      INLET = .FALSE.
      GAP = .FALSE.
      LINER = .FALSE.
      FOUL1 = 0.000D0
      FOUL2 = 0.000D0

      IOS = 0
      READ(14,'(A12)',ERR=100) COMMAND

      DO WHILE (IOS .EQ. 0)
         IF (COMMAND(1:1) .NE. '!') THEN
         IF (COMMAND .EQ. 'HEADER      ' .OR.
     *      COMMAND .EQ. 'header      ') THEN
             READ(14,'(A80)') HEADING

         ELSEIF (COMMAND .EQ. 'GIPS CALCULA' .OR.
     *      COMMAND .EQ. 'gips calcula') THEN
            READ(14,*,ERR=101) NGIPS

         ELSEIF (COMMAND .EQ. 'LENGTH        ' .OR.
     *      COMMAND .EQ. 'length        ') THEN
            READ(14,*,ERR=101) XF

         ELSEIF (COMMAND .EQ. 'PRINT FREQUE' .OR.
     *      COMMAND .EQ. 'print freque') THEN
            READ(14,*,ERR=101) NPR

         ELSEIF (COMMAND .EQ. 'INTEGRATION ' .OR.
     *      COMMAND .EQ. 'integration') THEN
            READ(14,*,ERR=101) NINT

         ELSEIF (COMMAND .EQ. 'TUBE DIMENSI' .OR.
     *      COMMAND .EQ. 'tube dimensi') THEN
            READ(14,*,ERR=101) DO,DI
            IF (DI .GE. DO) THEN
              WRITE(6,*) 'INNER DIAMETER LARGER THAN OUTER - STOP'
              PAUSE
            ENDIF

         ELSEIF (COMMAND .EQ. 'TUBE COUNT  ' .OR.
     *      COMMAND .EQ. 'tube count  ') THEN
            READ(14,*,ERR=101) NTUB

         ELSEIF (COMMAND .EQ. 'TOTAL FLOW  ' .OR.
     *      COMMAND .EQ. 'total flow  ') THEN
            READ(14,*,ERR=101) MPRIK

         ELSEIF (COMMAND .EQ. 'GAS TEMPERAT' .OR.
     *      COMMAND .EQ. 'gas temperat') THEN
            READ(14,*,ERR=101) TG1,TG2
            IF (TG2 .GE. TG1) THEN
              WRITE(6,*) 'GAS INLET LOWER THAN OUTLET - STOP'
              PAUSE
            ENDIF

         ELSEIF (COMMAND .EQ. 'SHELL FILM C' .OR.
     *      COMMAND .EQ. 'shell film c') THEN
            READ(14,*,ERR=101) HO1, HO2
            IF (HO2 .GE. HO1) THEN
             WRITE(6,*) 'SHELL SIDE FILM COEFFICIENTS UNEXPECTED - STOP'
             PAUSE
            ENDIF

         ELSEIF (COMMAND .EQ. 'TUBE FILM CO' .OR.
     *      COMMAND .EQ. 'tube film co') THEN
            READ(14,*,ERR=101) HI1, HI2
            IF (HI2 .GE. HI1) THEN
              WRITE(6,*) 'TUBE SIDE FILM COEFFICIENTS UNEXPECTED - STOP'
              PAUSE
            ENDIF

         ELSEIF (COMMAND .EQ. 'HEAT CAPACIT' .OR.
     *      COMMAND .EQ. 'heat capacit') THEN
            READ(14,*) CP1, CP2
              IF (CP2 .GE. CP1) THEN
              WRITE(6,*,ERR=101) 'HEAT CAPACITIES UNEXPECTED - STOP'
              PAUSE
            ENDIF

         ELSEIF (COMMAND .EQ. 'WATER TEMPER' .OR.
     *      COMMAND .EQ. 'water temper') THEN
            READ(14,*,ERR=101) TW

         ELSEIF (COMMAND .EQ. 'GAS DENSITY ' .OR.
     *      COMMAND .EQ. 'gas density ') THEN
            READ(14,*,ERR=101) RHO1

         ELSEIF (COMMAND .EQ. 'STEEL CONDUC' .OR.
     *      COMMAND .EQ. 'steel conduc') THEN
            READ(14,*,ERR=101) RL

         ELSEIF (COMMAND .EQ. 'GAS MOLECULA' .OR.
     *      COMMAND .EQ. 'gas molecula') THEN
            READ(14,*,ERR=101) W

         ELSEIF (COMMAND .EQ. 'SHELL SIDE F' .OR.
     *      COMMAND .EQ. 'shell side f') THEN
            READ(14,*,ERR=101) FOUL2

         ELSEIF (COMMAND .EQ. 'GAS CISCOSIT' .OR.
     *      COMMAND .EQ. 'gas viscosit') THEN
            READ(14,*,ERR=101) RMY1

         ELSEIF (COMMAND .EQ. 'TUBE SIDE FO' .OR.
     *      COMMAND .EQ. 'tube side fo') THEN
            READ(14,*,ERR=101) FOUL1

         ELSEIF (COMMAND .EQ. 'INCLUDE ENHA' .OR.
     *      COMMAND .EQ. 'include enha') THEN
            INLET = .TRUE.

         ELSEIF (COMMAND .EQ. 'INCLUDE GAP ' .OR.
     *      COMMAND .EQ. 'incluide gap ') THEN
            GAP = .TRUE.
            READ(14,*,ERR=101) TGAP,RGAP

         ELSEIF (COMMAND .EQ. 'INCLUDE LINE' .OR.
     *      COMMAND .EQ. 'include line') THEN
            LINER = .TRUE.
            READ(14,*,ERR=101) TLINER,RLINE

          ELSE
            WRITE(6,*) 'COMMAND ',COMMAND,' NOT UNDERSTOOD - STOP'
            PAUSE
         END IF

         ENDIF

         READ(14,'(A12)',IOSTAT=IOS) COMMAND

      ENDDO
      CLOSE(14)
      GOTO 102
  100 WRITE(6,*) ' INPUT FILE DOES NOT EXIST OR EMPTY'
  101 WRITE(6,*) ' INPUT NOT AS EXPECTED AFTER COMMAND:', COMMAND

C
C	DEFINE FLOW PER TUBE (kmol/hr) AND CALCULATED LINEAR PROFILE IN
C       IN CP, HI AND HO BASED ON INPUT GIPS INLET/OUTLET TEMPERATURES
C
  102 MPRIK = MPRIK/NTUB

      DTG  = TG1 - TG2
      DCP  = (CP1-CP2)/DTG
      DHI   = (HI1-HI2)/DTG
      DHO   = (HO1-HO2)/DTG
C
C     CONVERT FROM cP AND CALCULATE Re NUMBER

      RMY1 = RMY1*3.60d0
      QVOL = W*MPRIK/RHO1
      A1   = 0.785398D0*DI*DI
      V1   = 2.77777D-04*QVOL/A1
C
      RE1   = DI*V1*RHO1*3600/RMY1
      DII   = DI

C
C     ECHO INPUT FOR VERIFICATION
C
      WRITE(10,'(1X,A80)') HEADING
      WRITE(10,*) 'Based on GIPS calc. no. ',NGIPS
      WRITE(10,*) ' '
      WRITE(6,*) ' ******  INPUT PARAMETERS   ******'
      WRITE(6,*)
      WRITE(10,*) ' ******  INPUT PARAMETERS   ******'
      WRITE(10,*)
      WRITE(6,*) 'TUBE OD                 = ',DO
      WRITE(6,*) 'TUBE ID                 = ',DI
      WRITE(6,*) 'TUBE CONDUCTIVITY       = ',RL
      WRITE(10,*) 'TUBE OD                 = ',DO
      WRITE(10,*) 'TUBE ID                 = ',DI
      WRITE(10,*) 'TUBE CONDUCTIVITY       = ',RL
      WRITE(6,*) 'NUMBER OF TUBES         =  ',NTUB
      WRITE(6,*) 'FLOW PER TUBE           = ',MPRIK
      WRITE(6,*) 'MOLECULAR WEIGHT        = ',W
      WRITE(6,*) 'VISCOSITY (Kg/m hr)     = ',RMY1
      WRITE(6,*) 'GAS DESNITY             = ',RHO1
      WRITE(10,*) 'NUMBER OF TUBES         =  ',NTUB
      WRITE(10,*) 'FLOW PER TUBE           = ',MPRIK
      WRITE(10,*) 'MOLECULAR WEIGHT        = ',W
      WRITE(10,*) 'VISCOSITY (Kg/m hr)     = ',RMY1
      WRITE(10,*) 'GAS DESNITY             = ',RHO1

      WRITE(6,*) 'Temperature dependent input summary '
      WRITE(6,*) 'Position     Temperature       Cp     H(tube)',
     *           '    H(shell)'
      WRITE(6,'(A10,F12.2,F12.4,2F12.2)') ' Inlet   ',TG1,CP1,HI1,HO1
      WRITE(6,'(A10,F12.2,F12.4,2F12.2)') ' Outlet  ',TG2,CP2,HI2,HO2
      WRITE(10,*) 'Temperature dependent input summary '
      WRITE(10,*) 'Position     Temperature       Cp     H(tube)',
     *           '    H(shell)'
      WRITE(10,'(A10,F12.2,F12.4,2F12.2)') ' Inlet   ',TG1,CP1,HI1,HO1
      WRITE(10,'(A10,F12.2,F12.4,2F12.2)') ' Outlet  ',TG2,CP2,HI2,HO2
C
C	USE INLET CONDITION
C
      WRITE(6,*) 'FLOW SPEED AND REYNOLDS NUMBER AT INLET:', V1, RE1
      WRITE(10,*) 'FLOW SPEED AND REYNOLDS NUMBER AT INLET:', V1, RE1
C
C	DEFINE LINER AND GAP OPTIONS
C
      IF (GAP) THEN
	DIGAP  = DI - 2*TGAP
	DOGAP  = DI
      ENDIF

      IF (LINER) THEN
	IF (GAP) THEN
	  DOLIN  = DIGAP
	ELSE
	  DOLIN  = DI
	ENDIF
	DILIN  = DOLIN - 2*TLINER
      ENDIF
C
      WRITE(6,*) 'FOULING FACTOR INSIDE   = ', FOUL1
      WRITE(6,*) 'FOULING FACTOR, OUTSIDE = ', FOUL2
      IF (LINER) THEN
	  WRITE(6,*) 'WITH LINER '
	  WRITE(6,'('' OD = '',F8.5,'' ID = '',F8.5)') DOLIN,DILIN
	  WRITE(6,*) 'CONDUCTIVITY            = ',RLINE
      ELSE
	  WRITE(6,*) 'NO LINER '
      END IF
      IF (GAP) THEN
      WRITE(6,*) 'WITH GAP BETWEEN LINER AND TUBE '
      WRITE(6,'('' OD = '',F8.5,'' ID = '',F8.5)') DOGAP,DIGAP
	  WRITE(6,*) 'CONDUCTIVITY            = ',RGAP
      ELSE
	  WRITE(6,*) 'NO GAP BETWEEN LINER AND TUBE '
      END IF

      WRITE(10,*) 'FOULING FACTOR INSIDE   = ', FOUL1
      WRITE(10,*) 'FOULING FACTOR, OUTSIDE = ', FOUL2
      IF (LINER) THEN
	  WRITE(10,*) 'WITH LINER '
	  WRITE(10,'('' OD = '',F8.5,'' ID = '',F8.5)') DOLIN,DILIN
	  WRITE(10,*) 'CONDUCTIVITY            = ',RLINE
      ELSE
	  WRITE(10,*) 'NO LINER '
      END IF
      IF (GAP) THEN
	  WRITE(10,*) 'WITH GAP BETWEEN LINER AND TUBE '
          WRITE(10,'('' OD = '',F8.5,'' ID = '',F8.5)') DOGAP,DIGAP
	  WRITE(10,*) 'CONDUCTIVITY            = ',RGAP
      ELSE
	  WRITE(10,*) 'NO GAP BETWEEN LINER AND TUBE '
      END IF
      IF (INLET) THEN
		WRITE(6,*) 'INCREASED HEAT TRANSFER IN INLET APPLIED'
		WRITE(10,*) 'INCREASED HEAT TRANSFER IN INLET APPLIED'
      END IF

      WRITE(6,*)
      WRITE(6,*) ' *******  OUTPUT  ******** '
      WRITE(6,*) ' '
      WRITE(10,*)
      WRITE(10,*) ' *******  OUTPUT  ******** '
      WRITE(10,*) ' '

      RETURN
      END
	
C
      SUBROUTINE RUNKUT(X0,Y,NVAR,STEP,NSTEP)
C
C    This program solves an ordinary differential equation by means of
C    a 4th order Runge-Kutta method.
C
C    INPUT   
C            X0        Start value
C            Y         Vector of starting values
C            NVAR      Number of variables, length of Y
C            STEP      Step size
C            NSTEP     Number of steps
C
C
      IMPLICIT LOGICAL*1 (A-Z)
      INTEGER  NVAR,NSTEP,I,J
      REAL*8   X0,Y(NVAR),STEP
      REAL*8   K1(20),K2(20),K3(20),K4(20),Y1(20),X1
      REAL*8   STEPH,SJDEL
C
      STEPH = 0.5D0*STEP
      SJDEL = 1.0D0/6.0D0
C
      DO 50 I = 1,NSTEP
        CALL FCN(X0,Y,K1,NVAR)
        DO 10 J = 1,NVAR
          Y1(J) = Y(J) + STEPH*K1(J)
   10   CONTINUE
        X1  = X0 + STEPH
        CALL FCN(X1,Y1,K2,NVAR)
        DO 20 J = 1,NVAR
          Y1(J) = Y(J) + STEPH*K2(J)
   20   CONTINUE
        CALL FCN(X1,Y1,K3,NVAR)
        DO 30 J = 1,NVAR
          Y1(J) = Y(J) + STEP*K3(J)
   30   CONTINUE
        X1 = X0 + STEP
        CALL FCN(X1,Y1,K4,NVAR)
C
        DO 40 J = 1,NVAR
          Y(J) = Y(J) + SJDEL*STEP*(K1(J)+2*K2(J)+2*K3(J)+K4(J))
   40   CONTINUE
C
        X0  = X1
C       WRITE(6,'('' '',20E13.5)') X0,(Y(J),J=1,NVAR)
C
   50 CONTINUE
C
      RETURN
      END

      SUBROUTINE EVAL(X,TI,TM1,TM2,TMEAN,TLI,TLO,UALL)
C
C     Back calculated temperatures on tube surface and on liner if
C     applicable
C
      REAL*8  X,TI,TM1,TM2, TCHECK, TMEAN
      REAL*8  UALL,TW, DT1,DT2,DT3,DT4,DT5
      REAL*8  DI, DO, PI, RL, HI, HO
      REAL*8  R1, R2, R3, FOUL1, FOUL2, Q, DELTA
      REAL*8  MPRIK, CAP
      REAL*8  RIFOUL,ROFOUL,TLI,TLO
      REAL*8  DILIN,DOLIN,RLINE,RLI,DIGAP,DOGAP,RGAP,RLG
      REAL*8  XCOR,BETA
      REAL*8  TG1,CP1,DCP,HI1,DHI,HO1,DHO
      LOGICAL LINER,GAP,INLET
      INTEGER NVAR

      COMMON /ONE/ DI, DO, PI, TW, RL, HI, HO, MPRIK, CAP,
     *             FOUL1, FOUL2
      COMMON /TWO/ DILIN,DOLIN,RLINE,LINER,INLET
      COMMON /THREE/ DIGAP,DOGAP,RGAP,GAP
      COMMON /FIVE/ TG1,CP1,DCP,HI1,DHI,HO1,DHO
C
C     Correlate film coefficients to actual surface
C     Add liner properties if applicable
C     Add enhanced heat transfer in inlet if applicable
C
      HI    = (HI1 + DHI*(TI-TG1))*DO/DI
      HO    = HO1 + DHO*(TI-TG1)
      IF (LINER) HI = HI*(DI/DILIN)**1.6D0
      IF (INLET) THEN
	  XCOR = X + 0.12D0
	  CALL BETAFA(XCOR,BETA)
	  HI = HI*BETA
      END IF

      RIFOUL= 1.0D0/HI + FOUL1
      ROFOUL= 1.0D0/HO + FOUL2

      R1    = LOG(DO/DI)/(2*PI*RL)
      IF (LINER) THEN
	  R2    = RIFOUL/(PI*DILIN)
	  RLI   = LOG(DOLIN/DILIN)/(2*PI*RLINE)
      ELSE
	  R2    = RIFOUL/(PI*DI)
	  RLI   = 0.0D0
      END IF
      R3    = ROFOUL/(PI*DO)
      RLG  = 0.0D0
      IF (GAP) RLG = LOG(DOGAP/DIGAP)/(2*PI*RGAP)
		
      DELTA = (TI-TW)
		
      Q     = DELTA/(R1+R2+R3+RLI+RLG)
      UALL  = Q/(DELTA*PI*DO)
      DT1   = Q*R2
      DT2   = Q*RLI
      DT4   = R1*Q
      DT3   = RLG*Q
      DT5   = R3*Q

      TLI   = TI - DT1
      TLO   = TLI - DT2

      TM1   = TLO - DT3
      TM2   = TM1 - DT4

      TCHECK = TM2 - DT5
      TMEAN  = 0.5D0*(TM1+TM2)
C
C     Check temperature profile backclaculation is consistent
C
      IF (ABS(TCHECK-TW) .GT. 0.01D0) THEN
	  WRITE(6,*) ' CALCULATION ERROR'
	  WRITE(6,*) ' T CHECK NOT EQUAL TO TW '
	  WRITE(6,*) ' T CHECK = ',TCHECK
	  STOP
      END IF

      RETURN
      END

      SUBROUTINE EVALQ(TI,TOLD,UALL,UOLD,CAPO,DX,QTIL,QAVG,KODE)
C
C     Routine to backcalculate the transferred heat since the last call
C     First time (KODE = 1), only initialization takes place
C
C
      REAL*8  TI,TOLD,UOLD,CAPO,DX
      REAL*8  UALL, TW
      REAL*8  TAVG,UAVG,CAVG,QTIL,QAVG
      REAL*8  DI, DO, PI, RL, HI, HO
      REAL*8  R1, R2, R3, FOUL1, FOUL2
      REAL*8  MPRIK, CAP
      REAL*8  TG1,CP1,DCP,HI1,DHI,HO1,DHO
      INTEGER KODE

      COMMON /ONE/ DI, DO, PI, TW, RL, HI, HO, MPRIK, CAP,
     *             FOUL1, FOUL2
      COMMON /FIVE/ TG1,CP1,DCP,HI1,DHI,HO1,DHO
	  
      IF (KODE .EQ. 2) THEN
	  TAVG = 0.5D0*(TI+TOLD)
	  UAVG = 0.5D0*(UOLD+UALL)
	  QTIL = DX*PI*DO*UAVG*(TAVG-TW)
	  CAVG = 0.5D0*(CAPO+CAP)
	  QAVG = (TOLD-TI)*CAVG*MPRIK
      END IF

      TOLD = TI
      UOLD = UALL
      CAPO = CP1 + DCP*(TI-TG1)
	  	
      RETURN
      END

      SUBROUTINE FCN(X,T,K,NVAL)
C
C     Subprogram cslculating the right hand side in the 1. oreder
C     differential equation, i.e. dT/dx = Q/(m Cp)
C
      REAL*8  X,T(20), K(20)
      REAL*8  UALL,TW
      REAL*8  DI, DO, PI, RL, HI, HO, MPRIK, CAP
      REAL*8  R1, R2, R3, FOUL1, FOUL2, Q, DELTA
      REAL*8  RIFOUL, ROFOUL
      REAL*8  DILIN,DOLIN,RLINE,RLI,DIGAP,DOGAP,RGAP,RLG
      REAL*8  XCOR,BETA
      REAL*8  TG1,CP1,DCP,HI1,DHI,HO1,DHO
      LOGICAL LINER,GAP,INLET
      INTEGER NVAR

      COMMON /ONE/ DI, DO, PI, TW, RL, HI, HO, MPRIK, CAP,
     *             FOUL1, FOUL2
      COMMON /TWO/ DILIN,DOLIN,RLINE,LINER,INLET
      COMMON /THREE/ DIGAP,DOGAP,RGAP,GAP
      COMMON /FIVE/ TG1,CP1,DCP,HI1,DHI,HO1,DHO

      HI    = (HI1 + DHI*(T(1)-TG1))*DO/DI
      HO    = HO1 + DHO*(T(1)-TG1)
      IF (LINER) HI = HI*(DI/DILIN)**1.6D0
      IF (INLET) THEN
	  XCOR = X + 0.12D0
	  CALL BETAFA(XCOR,BETA) 
	  HI = HI*BETA
      END IF


      RIFOUL= 1.0D0/HI + FOUL1
      ROFOUL= 1.0D0/HO + FOUL2

      R1    = LOG(DO/DI)/(2*PI*RL)
      IF (LINER) THEN
        R2    = RIFOUL/(PI*DILIN)
        RLI   = LOG(DOLIN/DILIN)/(2*PI*RLINE)
      ELSE
	  R2    = RIFOUL/(PI*DI)
	  RLI   = 0.0D0
      END IF

      RLG  = 0.0D0
      IF (GAP) RLG = LOG(DOGAP/DIGAP)/(2*PI*RGAP)
	
      R3    = ROFOUL/(PI*DO)
      DELTA = (T(1)-TW)
		
      Q     = DELTA/(R1+R2+R3+RLI+RLG)
	
      CAP   = CP1 + DCP*(T(1)-TG1)
      K(1)  = -Q/(MPRIK*CAP)
	
      RETURN
      END

      SUBROUTINE BETAFA(X,BETA)
C
C     Calculate heat transfer enhancement. Tube is assumed to to have an
C     inlet located 0.12 m before the tube simulation starts under the
C     assumption that refractory and tube sheet is present
C
      REAL*8 X, BETA, DI, RE1
C
      COMMON /FOUR/ RE1, DI
C
      IF (X .LE. 0.0D0) THEN
	  WRITE(6,*) ' ERROR - X EQUAL TO OR LESS THAN ZERO '
	  STOP
      ENDIF
C
      IF (X/DI .GT. 0.75D0) THEN
        BETA = 1 + 0.90D0*DI/X
      ELSE
        BETA = 2.20D0
      ENDIF
C
      RETURN
      END
