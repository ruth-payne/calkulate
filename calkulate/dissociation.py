# Calkulate: seawater total alkalinity from titration data
# Copyright (C) 2019  Matthew Paul Humphreys  (GNU GPLv3)

from numpy import exp, log


# ===== COMBINED KX LISTS =====================================================

# --- DSC07 best practice, Free scale -----------------------------------------

def KX_F(tempK, psal, ST, FT):

    # Evaluate dissociation coefficients
    KC1_T, KC2_T = KC_T_LDK00(tempK, psal) # Total
    KB_T = KB_T_D90a(tempK, psal) # Total
    KH2O_T = KH2O_T_DSC07(tempK, psal) # Total
    KHSO4_F = KHSO4_F_D90b(tempK, psal) # Free
    KHF_T = KHF_T_PF87(tempK, psal) # Total
    KP1_T, KP2_T, KP3_T = KP_T_DSC07(tempK, psal) # Total
    KSi_T = KSi_T_M95(tempK, psal) # Total

    # Get pH scale conversion factors
    T2F = 1 / (1 + ST / KHSO4_F)

    # Convert everything to Free pH scale
    KC1_F  = KC1_T * T2F
    KC2_F = KC2_T * T2F
    KB_F = KB_T * T2F
    KH2O_F = KH2O_T * T2F
    KHF_F = KHF_T * T2F
    KP1_F = KP1_T * T2F
    KP2_F = KP2_T * T2F
    KP3_F = KP3_T * T2F
    KSi_F = KSi_T * T2F

    return [KC1_F, KC2_F, KB_F, KH2O_F, KHSO4_F, KHF_F, KP1_F, KP2_F, KP3_F,
        KSi_F]


# ===== IONIC STRENGTH ========================================================


def Istr(psal):
    return 19.924 * psal / (1000 - 1.005 * psal)


# ===== CARBONIC ACID =========================================================

# --- Lueker et al. (2000) ----------------------------------------------------
#
# Mar Chem 70(1-3), 105-119, doi:10.1016/S0304-4203(00)00022-0
#
# Total pH scale
#
#  2 < T < 35 degC
# 19 < S < 43

def KC_T_LDK00(tempK, psal):

    # LDK00 Eq. (16)
    pK_T_C1 = 3633.86 / tempK \
            -   61.2172 \
            +    9.6777 * log(tempK) \
            -    0.011555 * psal \
            +    0.0001152 * psal**2

    # LDK00 Eq. (17)
    pK_T_C2 =  471.78 / tempK \
            +   25.929 \
            -    3.16967 * log(tempK) \
            -    0.01781 * psal \
            +    0.0001122 * psal**2

    return 10**-pK_T_C1, 10**-pK_T_C2


# ===== BORIC ACID ============================================================

# --- Dickson (1990a) ---------------------------------------------------------
#
# Deep-Sea Res Pt A 37(5), 755-766, doi:10.1016/0198-0149(90)90004-F
#
# Total pH scale
#
#  0 < T < 45 degC
#  5 < S < 45

def KB_T_D90a(tempK, psal):

    # D90a Eq. (23)
    ln_KB =   ( - 8966.90                        \
                - 2890.53   * psal**0.5             \
                -   77.942  * psal                  \
                +    1.728  * psal**1.5             \
                -    0.0996 * psal**2   ) / tempK  \
            + 148.0248                           \
            + 137.1942  * psal**0.5                 \
            +   1.62142 * psal                      \
            - (     24.4344                      \
                +   25.085  * psal**0.5             \
                +    0.2474 * psal      ) * log(tempK) \
            +   0.053105    * psal**0.5   *     tempK

    return exp(ln_KB)


# ===== WATER =================================================================

# --- Dickson et al. (2007) ---------------------------------------------------
#
# PICES Special Publication 3
#
# Total pH scale

def KH2O_T_DSC07(tempK, psal):

    ln_KH2O =     148.9652                        \
              - 13847.26    /     tempK              \
              -    23.6521  * log(tempK)             \
              + (   118.67   /     tempK             \
                  -   5.977                       \
                  +   1.0495 * log(tempK) ) * psal**0.5 \
              - 0.01615 * psal

    return exp(ln_KH2O)


# ===== BISULFATE =============================================================

# --- Dickson (1990b) ---------------------------------------------------------
#
# J Chem Thermodyn 22(2), 113-127, doi:10.1016/0021-9614(90)90074-Z
#
# Free pH scale
#
#  0 < T < 45 degC
#  5 < S < 45

def KHSO4_F_D90b(tempK, psal):

    # Ionic strength
    I = Istr(psal)

    # D90b Eqs. (22) & (23)
    ln_KHSO4 = - 4276.1   /     tempK                  \
               +  141.328                           \
               -   23.093 * log(tempK)                 \
               + ( - 13856     /     tempK             \
                   +   324.57                       \
                   -    47.986 * log(tempK) ) * I**0.5 \
               + (   35474     /     tempK             \
                   -   771.54                       \
                   +   114.723 * log(tempK) ) * I      \
               - (    2698     /     tempK)   * I**1.5 \
               + (    1776     /     tempK)   * I**2   \
               + log(1 - 0.001005 * psal)

    return exp(ln_KHSO4)


# ===== HYDROGEN FLUORIDE =====================================================

# --- Perez & Fraga (1987) ----------------------------------------------------
#
# Mar Chem 21(2), 161-168, doi:10.1016/0304-4203(87)90036-3
#
# Total pH scale
#
#  9 < T < 33 degC
# 10 < S < 40

def KHF_T_PF87(tempK, psal):

    ln_KHF = - ( - 874     / tempK        \
                 -   0.111 * psal**0.5   \
                 +   9.68            )

    return exp(ln_KHF)


# --- Dickson & Riley (1979) --------------------------------------------------
#
# Mar Chem 7(2), 101-109, doi:10.1016/0304-4203(79)90002-1
#
# Free pH scale
#
#  5 < T < 35 degC
# 10 < S < 48

def KHF_F_DR79(tempK, psal):

    # Ionic strength
    I = Istr(psal)

    # Evaluate HF dissociation constant
    ln_KF =   1590.2   / tempK       \
            -   12.641            \
            +    1.525 * I **0.5  \
            + log(1 - 0.001005*psal)

    return exp(ln_KF)


# ===== PHOSPHORIC ACID =======================================================

# --- Dickson et al. (2007) ---------------------------------------------------
#
# PICES Special Publication 3
#
# Total pH scale

def KP_T_DSC07(tempK, psal):

    # KP1 = [H+][H2PO4-]/[H3PO4]
    ln_KP1 = - 4576.752 /     tempK            \
            +  115.525                     \
            -   18.453 * log(tempK)           \
            + (- 106.736    / tempK           \
               +   0.69171      ) * psal**0.5 \
            + (-   0.65643 / tempK            \
               -   0.01844      ) * psal

    # KP2 = [H+][HPO42-]/[H2PO4-]
    ln_KP2 = - 8814.715 /     tempK           \
            +  172.0883                   \
            -   27.927 * log(tempK)          \
            + (- 160.34    / tempK           \
               +   1.3566      ) * psal**0.5 \
            + (    0.37335 / tempK           \
               -   0.05778     ) * psal

    # KP3 = [H+][PO43-]/[HPO42-]
    ln_KP3 = - 3070.75 / tempK               \
            - 18.141                     \
            + (  17.27039 / tempK           \
               +  2.81197     ) * psal**0.5 \
            + (- 44.99486 / tempK           \
               -  0.09984     ) * psal

    return exp(ln_KP1), exp(ln_KP2), exp(ln_KP3)


# ===== SILICIC ACID ==========================================================

# --- Millero (1995) ----------------------------------------------------------
#
#
#
# via Dickson et al. (2007)

def KSi_T_M95(tempK, psal):

    # Ionic strength
    I = 19.924 * psal / (1000 - 1.005 * psal)

    #  KSi = [SiO((OH)3)-] [H+] / [Si(OH)4]
    ln_KSi = - 8904.2   /     tempK   \
             +  117.385            \
             -   19.334 * log(tempK)  \
             + ( - 458.79    / tempK   \
                 +   3.5913       ) * I**0.5 \
             + (   188.74    / tempK            \
                 -   1.5998       ) * I      \
             + ( -  12.1652  / tempK            \
                 +   0.07871      ) * I**2   \
             + log(1 - 0.001005 * psal)

    return exp(ln_KSi)


# ===== AMMONIUM ==============================================================

# --- Bell et al. (2008) ------------------------------------------------------
#
# Environ Chem 5, 258, doi:10.1071/EN07032_CO
#
# pH scale unclear

def KNH4_X_BJJL08(tempK, psal):

    # BJJL08 Eq. (3)
    pKNH4 = 10.0423 - \
        0.0315536 * tempK + \
        0.003071 * psal

    return 10**-pKNH4


# ===== 2-AMINOPYRIDINE =======================================================

# --- Bates & Erickson (1986) -------------------------------------------------
#
# J Solution Chem 15(11), 891-901, doi:10.1007/BF00646030
#
# Stoichiometric dissociation constant
#
# Seawater pH scale
#
#  5 < T < 40 degC
# 30 < S < 40

def K2AMP_S_BE86(tempK, psal):

    # BE86 Eq. (10)
    pK_S_2AMP =   2498.31   /     tempK        \
                -   15.3274                 \
                +    2.4050 * log(tempK)       \
                + (   0.012929              \
                    - 2.9417e-5 * tempK  ) * psal

    return 10**-pK_S_2AMP