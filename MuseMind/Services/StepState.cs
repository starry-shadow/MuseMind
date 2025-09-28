using System;

namespace MuseMind.Services
{
    public class StepState
    {
        public event Action? OnChange;
        private int _currentStep = 1;
        public int CurrentStep
        {
            get => _currentStep;
            set
            {
                if (_currentStep != value)
                {
                    _currentStep = value;
                    OnChange?.Invoke();
                }
            }
        }
    }
}
