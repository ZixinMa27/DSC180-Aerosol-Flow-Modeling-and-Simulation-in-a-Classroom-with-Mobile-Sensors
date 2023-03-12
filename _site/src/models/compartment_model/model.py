import numpy as np
from scipy.integrate import solve_ivp
from scipy.integrate import odeint


class CompartmentModel:
    def __init__(self, num_sub_compartment, Vp, Q, Vs: list, alphas: list, betas: list, aerosol_mass_gen_rates: list, aerosol_mass_func=None):
        self.num_sub_compartment = num_sub_compartment

        # self.room_dims = room_dims
        # self.sub_compartment_dims = sub_compartment_dims
        # assert len(room_dims) == 3, 'Please provide room dimensions as "[l,w,h]"'
        # assert len(sub_compartment_dims) == 3, 'Please provide sub compartment dimensions as "[l,w,h]"'
        # self.Vs = sub_compartment_dims[0]*sub_compartment_dims[1]*sub_compartment_dims[2]
        # self.Vp = room_dims[0]*room_dims[1]*room_dims[2] - self.Vs
        self.Vp = Vp
        self.Vs = Vs

        self.Q = Q
        self.alphas = alphas
        self.betas = betas
        self.aerosol_mass_gen_rate = aerosol_mass_gen_rates
        self.aerosol_mass_func = aerosol_mass_func
        

    def setup_equations(self, init_vals):
        self.diff_eqn = self._dSdt
        self.init_vals = init_vals
        

    def _dSdt(self, t, S):
        print(t)
        Cp = S[0]
        Cs = S[1:]

        dSdt = [None]*(self.num_sub_compartment+1)

        _dCpdt = 0
        _dCpdt_last_term_coef = 1
        for i in range(self.num_sub_compartment):
            if self.aerosol_mass_func != None:
                _dCsdt = self.alphas[i]*self.Q*Cp - self.alphas[i]*(1-self.betas[i])*self.Q*Cs[i] - self.alphas[i]*self.betas[i]*self.Q*Cs[i] + self.aerosol_mass_func[i].get_rate(t)
            else:
                _dCsdt = self.alphas[i]*self.Q*Cp - self.alphas[i]*(1-self.betas[i])*self.Q*Cs[i] - self.alphas[i]*self.betas[i]*self.Q*Cs[i] + self.aerosol_mass_gen_rate[i]
            dSdt[i+1] = _dCsdt/self.Vs[i]

            #primary compartment term
            _dCpdt = _dCpdt - self.alphas[i]*self.Q*Cp + self.alphas[i]*(1-self.betas[i])*self.Q*Cs[i]
            _dCpdt_last_term_coef -= self.alphas[i]*self.betas[i]

        dSdt[0] = (_dCpdt - _dCpdt_last_term_coef*self.Q*Cp)/self.Vp

        return dSdt

    def simulate(self, time_span, solver='ivp'):
        if solver == 'odeint':
            return odeint(self.diff_eqn, t= time_span, y0=self.init_vals, tfirst=True)
        else:
            return solve_ivp(self.diff_eqn, t_span=(0, max(time_span)), y0=self.init_vals)



class AerosolSourceSimulation:
    def __init__(self, type, time_window):
        self.type = type
        self.time_window = time_window
        self.divide_count = 10
        self.total_particle = 300000000
        self.counter = 0

    def get_rate(self,t):
        if self.type == 'cough':
            self.counter += 1
            if self.counter <= self.divide_count:
                return self.total_particle/self.divide_count
            else:
                return 0
        else:
            return 0
        

class TwoCompartmentModel:
    def __init__(self, Vp, Vs, Q, alpha, beta, aerosol_mass_gen_rate):
        self.num_sub_compartment = 1
        # self.room_dims = room_dims
        # self.sub_compartment_dims = sub_compartment_dims
        # assert len(room_dims) == 3, 'Please provide room dimensions as "[l,w,h]"'
        # assert len(sub_compartment_dims) == 3, 'Please provide sub compartment dimensions as "[l,w,h]"'
        # self.Vs = sub_compartment_dims[0]*sub_compartment_dims[1]*sub_compartment_dims[2]
        # self.Vp = room_dims[0]*room_dims[1]*room_dims[2] - self.Vs
        self.Vp = Vp
        self.Vs = Vs

        self.Q = Q
        self.alpha = alpha
        self.beta = beta
        self.aerosol_mass_gen_rate = aerosol_mass_gen_rate
        

    def setup_equations(self, init_vals):
        #no channeling
        self.diff_eqn = self._dSdt
        self.init_vals = init_vals
        

    def _dSdt_noBeta(self, t, S, *args):
        Cp, Cs = S

        dCpdt = (-self.Q*Cp + self.alpha*self.Q*(Cs-Cp))/self.Vp
        dCsdt = (self.alpha*self.Q*(Cp-Cs) + self.aerosol_mass_gen_rate)/self.Vs

        return [dCpdt, dCsdt]

    def _dSdt(self, t, S):
        Cp, Cs = S

        dCpdt = (self.alpha*(1-self.beta)*self.Q*Cs - self.alpha*self.Q*Cp - (1-self.alpha*self.beta)*self.Q*Cp)/self.Vp
        dCsdt = (self.alpha*self.Q*Cp - self.alpha*(1-self.beta)*self.Q*Cs - self.alpha*self.beta*self.Q*Cs + self.aerosol_mass_gen_rate)/self.Vs

        return [dCpdt, dCsdt]

    def simulate(self, time_span):
        return solve_ivp(self.diff_eqn, t_span=time_span, y0=self.init_vals)