def search(*search_mods):

        list_to_use = []

        job_list = []
        exp_list = []
        minimum_salary = ''
        
        #search the arguments provided for options
        for mod in search_mods:

            if option == '-jobs' or option == '-j':
                list_to_use = job_list

            elif option == '-experience' or option == '-e':
                list_to_use = exp_list

            elif option == '-salary' or option == '-s':
                list_to_use = minimum_salary

            else:
                #if this is the case, the last argument told us to set the minimum salary
                if type(list_to_use) == type(''):
                    list_to_use = mod

                #Otherwise, add the mod to one of the lists 
                else:
                    list_to_use.append(mod)

    #Returns the url to search

                    #modifiers for search()
        self.search_params = ['-jobtype', '-j','-salary', '-s', '-experience', '-e']
        self.valid_job_types = ['fulltime','contract','internship','temporary', 'parttime', 'commission']
        self.valid_experience_levels = ['entry_level', 'mid_level', 'senior_level']
